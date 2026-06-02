"""
AstroDome - Ecossistema Fechado de Suporte a Vida
Modulo principal de gerenciamento da estufa espacial
"""

import os
import json
from datetime import datetime


# ── Configuracoes (via variaveis de ambiente - NUNCA hardcoded) ──
NASA_API_KEY        = os.environ.get("NASA_API_KEY", "")
TELEMETRY_DB_PASS   = os.environ.get("TELEMETRY_DB_PASSWORD", "")
ORBITAL_API_TOKEN   = os.environ.get("ORBITAL_API_TOKEN", "")


# ── Pilar 1: Mapeamento Orbital ──────────────────────────────────
def mapear_oasis_espacial(planeta: str) -> dict:
    """
    Analisa dados orbitais para identificar zonas seguras de colonizacao.
    Procura crateras, tubos de lava, incidencia solar e gelo subterraneo.
    """
    zonas = {
        "lua": {
            "zona_recomendada": "Polo Sul Lunar",
            "protecao_radiacao": "Cratera Shackleton",
            "incidencia_solar": "92%",
            "gelo_subterraneo": True,
        },
        "marte": {
            "zona_recomendada": "Valles Marineris",
            "protecao_radiacao": "Tubo de lava detectado",
            "incidencia_solar": "43%",
            "gelo_subterraneo": True,
        },
    }
    return zonas.get(planeta.lower(), {"erro": "Planeta nao mapeado"})


# ── Pilar 2: Monitoramento Interno da Estufa ─────────────────────
class MonitorEstufa:
    """Gerencia os sensores internos do biodome."""

    LIMITES = {
        "temperatura_min": 18.0,
        "temperatura_max": 28.0,
        "co2_max_ppm":     1200,
        "umidade_min":     55,
        "pressao_min":     95.0,
    }

    def verificar_sensores(self, leitura: dict) -> list:
        """Retorna lista de alertas com base nas leituras dos sensores."""
        alertas = []

        temp = leitura.get("temperatura", 0)
        if not (self.LIMITES["temperatura_min"] <= temp <= self.LIMITES["temperatura_max"]):
            alertas.append(f"ALERTA: Temperatura fora do range: {temp}C")

        co2 = leitura.get("co2_ppm", 0)
        if co2 > self.LIMITES["co2_max_ppm"]:
            alertas.append(f"ALERTA: CO2 elevado: {co2} ppm")

        umidade = leitura.get("umidade", 0)
        if umidade < self.LIMITES["umidade_min"]:
            alertas.append(f"ALERTA: Umidade baixa: {umidade}%")

        pressao = leitura.get("pressao_kpa", 0)
        if pressao < self.LIMITES["pressao_min"]:
            alertas.append(f"ALERTA CRITICO: Pressao critica: {pressao} kPa")

        return alertas if alertas else ["Sistema: Todos os sensores normais"]


# ── Pilar 3: Inteligencia Botanica ──────────────────────────────
class AnalisadorPlantas:
    """Analisa o estado das plantas via visao computacional."""

    INDICADORES_COLHEITA = {
        "batata":   {"dias_ciclo": 90,  "cor_ideal": "amarelo-palha"},
        "soja":     {"dias_ciclo": 120, "cor_ideal": "amarelo-dourado"},
        "alface":   {"dias_ciclo": 45,  "cor_ideal": "verde-vibrante"},
        "espinafre":{"dias_ciclo": 40,  "cor_ideal": "verde-escuro"},
    }

    def avaliar_colheita(self, cultura: str, dias_plantio: int) -> str:
        """Avalia se a cultura atingiu o pico nutricional."""
        info = self.INDICADORES_COLHEITA.get(cultura.lower())
        if not info:
            return f"Cultura '{cultura}' nao cadastrada no sistema."

        progresso = (dias_plantio / info["dias_ciclo"]) * 100

        if progresso >= 95:
            return (f"COLHEITA: {cultura.upper()} atingiu pico nutricional! "
                    f"Cor esperada: {info['cor_ideal']}. Colher imediatamente.")
        elif progresso >= 80:
            return f"ATENCAO: {cultura.upper()} a {progresso:.0f}% do ciclo. Monitorar diariamente."
        else:
            return f"INFO: {cultura.upper()} a {progresso:.0f}% do ciclo. Crescimento normal."

    def detectar_anomalia(self, leitura_visual: dict) -> str:
        """Detecta fungos, pragas ou estresse hidrico nas folhas."""
        cor        = leitura_visual.get("cor_folha", "")
        manchas    = leitura_visual.get("manchas", False)
        murcha     = leitura_visual.get("murcha", False)

        if manchas:
            return "RISCO: Possivel fungo detectado. Isolar setor e aplicar tratamento."
        if murcha:
            return "ALERTA: Estresse hidrico detectado. Aumentar irrigacao."
        if "amarelo" in cor.lower():
            return "ATENCAO: Folhas amareladas. Verificar niveis de nitrogenio."
        return "OK: Planta saudavel."


# ── Pilar 4: Painel de Comando ───────────────────────────────────
class PainelColonia:
    """Interface de controle para os colonos."""

    RECEITAS = {
        "batata":    {"irrigacao_ml": 500, "luz_horas": 14, "temp_ideal": 20},
        "soja":      {"irrigacao_ml": 400, "luz_horas": 16, "temp_ideal": 25},
        "alface":    {"irrigacao_ml": 300, "luz_horas": 12, "temp_ideal": 18},
        "espinafre": {"irrigacao_ml": 350, "luz_horas": 12, "temp_ideal": 18},
    }

    def configurar_cultura(self, cultura: str) -> dict:
        """Reconfigura a estufa para uma nova receita de cultivo."""
        receita = self.RECEITAS.get(cultura.lower())
        if not receita:
            return {"erro": f"Receita para '{cultura}' nao encontrada."}

        return {
            "status":    "Estufa reconfigurada com sucesso",
            "cultura":   cultura,
            "irrigacao": f"{receita['irrigacao_ml']} ml/dia",
            "luz":       f"{receita['luz_horas']}h de fotoperiodo",
            "temperatura":f"{receita['temp_ideal']}C",
            "timestamp": datetime.utcnow().isoformat(),
        }

    def gerar_relatorio(self, setor: str, sensores: dict, cultura: str, dias: int) -> str:
        """Gera resumo executivo para o tablet do colono."""
        monitor   = MonitorEstufa()
        analisador = AnalisadorPlantas()

        alertas   = monitor.verificar_sensores(sensores)
        colheita  = analisador.avaliar_colheita(cultura, dias)

        linhas = [
            f"=== RELATORIO ASTRODOME - Setor {setor.upper()} ===",
            f"Cultura: {cultura} | Dia {dias} do ciclo",
            "",
            "-- Sensores --",
        ]
        linhas += alertas
        linhas += ["", "-- Botanica --", colheita]
        return "\n".join(linhas)


# ── Execucao de demonstracao ─────────────────────────────────────
if __name__ == "__main__":
    print("=== AstroDome Iniciando ===\n")

    # Pilar 1
    zona = mapear_oasis_espacial("lua")
    print(f"Zona recomendada na Lua: {zona['zona_recomendada']}")

    # Pilares 2-4
    painel   = PainelColonia()
    config   = painel.configurar_cultura("batata")
    print(f"\n{json.dumps(config, indent=2, ensure_ascii=False)}")

    leitura = {"temperatura": 22.5, "co2_ppm": 800, "umidade": 65, "pressao_kpa": 101.3}
    relatorio = painel.gerar_relatorio("B", leitura, "batata", 87)
    print(f"\n{relatorio}")
