import json
import os
import socket
import time
from googleapiclient.discovery import build
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi

socket.setdefaulttimeout(20)

YOUTUBE_KEY = os.environ["YOUTUBE_API_KEY"]
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

youtube = build("youtube", "v3", developerKey=YOUTUBE_KEY)
client = genai.Client(api_key=GEMINI_KEY)

with open("data/hardware.json", "r", encoding="utf-8") as f:
    hardware = json.load(f)

with open("data/benchmarks.json", "r", encoding="utf-8") as f:
    benchmarks = json.load(f)

def buscar_video_youtube(cpu_name, gpu_name):
    query = f"{cpu_name} {gpu_name} benchmark gaming test fps"
    for tentativa in range(3):
        try:
            req = youtube.search().list(
                q=query, part="snippet", type="video", maxResults=3, relevanceLanguage="en"
            )
            res = req.execute(num_retries=2)
            return res.get("items", [])
        except Exception as e:
            if "429" in str(e) or "quotaExceeded" in str(e):
                print("  Cota diária do YouTube atingida. Encerrando por hoje.")
                raise SystemExit(0)
            print(f"  Falha de rede no YouTube (tentativa {tentativa + 1}/3): {e}")
            time.sleep(5)
    return []

def extrair_dados_com_ia(video_id, titulo, descricao):
    legenda = ""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "pt"])
        legenda = " ".join([t["text"] for t in transcript])[:4000]
    except Exception:
        pass

    prompt = f"""
    Analise os dados deste vídeo de benchmark de hardware e extraia a média de FPS se houver menção a:
    cyberpunk (Cyberpunk 2077), cs2 (Counter-Strike 2), gtav (GTA V), valorant (Valorant).

    Título: {titulo}
    Descrição: {descricao}
    Legenda: {legenda}

    Retorne APENAS um JSON válido neste formato (omita jogos não mencionados):
    {{
      "videoUrl": "https://www.youtube.com/watch?v={video_id}",
      "titulo": "{titulo}",
      "jogos": {{
        "cyberpunk": {{"1080p": 100, "1440p": 70}},
        "cs2": {{"1080p": 300}}
      }}
    }}
    """

    # Tenta até 3 vezes se der erro 503 UNAVAILABLE
    for tentativa in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"  Servidor ocupado (tentativa {tentativa + 1}/3). Aguardando 10s...")
                time.sleep(10)
            else:
                raise e
    raise Exception("Servidor indisponível após 3 tentativas.")

for cpu in hardware["cpu"]:
    for gpu in hardware["gpu"]:
        combo_key = f"{cpu['id']}_{gpu['id']}"

        if combo_key in benchmarks:
            continue

        print(f"Buscando benchmark para: {cpu['name']} + {gpu['name']}...")
        videos = buscar_video_youtube(cpu["name"], gpu["name"])

        if videos:
            vid = videos[0]
            vid_id = vid["id"]["videoId"]
            titulo = vid["snippet"]["title"]
            desc = vid["snippet"]["description"]

            try:
                dados = extrair_dados_com_ia(vid_id, titulo, desc)
                benchmarks[combo_key] = dados

                # Salva imediatamente no arquivo após cada sucesso
                with open("data/benchmarks.json", "w", encoding="utf-8") as f:
                    json.dump(benchmarks, f, indent=2, ensure_ascii=False)
                print(f"  Salvo: {combo_key}")
            except Exception as e:
                print(f"  Erro na IA para {combo_key}: {e}")

        time.sleep(4)  # Pausa para não sobrecarregar a API

print("Processo finalizado!")