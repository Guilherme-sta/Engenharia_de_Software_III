def ha_sobreposicao(inicio_a: str, fim_a: str, inicio_b: str, fim_b: str) -> bool:
    """Regra RN-02: dois intervalos HH:MM se sobrepoem quando nenhum termina
    antes (ou no momento) do inicio do outro. Ponto unico da regra de horario."""
    return not (fim_a <= inicio_b or inicio_a >= fim_b)
