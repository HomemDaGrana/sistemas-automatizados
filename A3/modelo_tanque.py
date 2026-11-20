"""Modelo de referência com tempo virtual. Não implementa nem simula um CLP real."""
from dataclasses import dataclass, field

@dataclass
class Entradas:
    start: bool = False
    stop_ok: bool = True
    emg_ok: bool = True
    ol_ok: bool = True
    fonte_ok: bool = True
    minimo: bool = False
    maximo: bool = False
    hh: bool = False
    retorno: bool = False
    reset: bool = False

@dataclass
class Tanque:
    auto: bool = False
    enchendo: bool = False
    comando: bool = False
    pronto: bool = False
    ciclos: int = 0
    falhas: set = field(default_factory=set)
    tempo_pronto: float = 0.0
    tempo_enchendo: float = 0.0
    tempo_divergencia: float = 0.0
    start_anterior: bool = False
    reset_anterior: bool = False

    def passo(self, e: Entradas, dt: float = 0.1):
        if dt < 0:
            raise ValueError('Tempo virtual deve ser não negativo')
        start_edge = e.start and not self.start_anterior
        reset_edge = e.reset and not self.reset_anterior
        self.start_anterior, self.reset_anterior = e.start, e.reset
        coerente = not ((e.maximo and not e.minimo) or (e.hh and not e.maximo))
        for normal, causa in [(e.emg_ok,'EMERGENCIA'),(e.ol_ok,'SOBRECARGA'),
                              (e.fonte_ok,'SEM_AGUA_NA_FONTE'),(coerente,'SENSORES_INCOERENTES'),
                              (not e.hh,'ALTO_ALTO')]:
            if not normal:
                self.falhas.add(causa)
        seguro = e.emg_ok and e.ol_ok and e.fonte_ok and coerente and not e.hh
        if self.falhas:
            self.auto = self.enchendo = False
        if reset_edge and seguro and e.stop_ok and not e.start and not e.retorno:
            self.falhas.clear()
            self.auto = self.enchendo = False
            self.tempo_pronto = self.tempo_enchendo = self.tempo_divergencia = 0.0
            self.pronto = False
        # O scan de RESET não acumula o tempo de prontidão.
        if seguro and e.stop_ok and not self.falhas and not reset_edge:
            self.tempo_pronto += dt
        else:
            self.tempo_pronto = 0.0
        self.pronto = self.tempo_pronto >= 3.0
        if not e.stop_ok:
            self.auto = self.enchendo = False
        elif start_edge and self.pronto and not self.falhas:
            self.auto = True
        concluido = False
        if self.auto and not self.falhas:
            if e.maximo:
                concluido = self.enchendo
                self.enchendo = False
            elif not e.minimo:
                self.enchendo = True
        else:
            self.enchendo = False
        if self.enchendo:
            self.tempo_enchendo += dt
        else:
            self.tempo_enchendo = 0.0
        if self.tempo_enchendo >= 30.0:
            self.falhas.add('TEMPO_MAXIMO')
        self.comando = self.auto and self.enchendo and seguro and e.stop_ok and not self.falhas
        if self.comando != e.retorno:
            self.tempo_divergencia += dt
        else:
            self.tempo_divergencia = 0.0
        if self.tempo_divergencia >= 2.0:
            self.falhas.add('RETORNO_DIVERGENTE')
        if self.falhas:
            self.auto = self.enchendo = self.comando = self.pronto = False
            self.tempo_pronto = 0.0
        elif concluido:
            self.ciclos += 1
        return self.estado

    @property
    def estado(self):
        if self.falhas: return 'FALHA'
        if self.comando: return 'ENCHENDO'
        if self.auto: return 'AGUARDANDO_NIVEL'
        if self.pronto: return 'PRONTO'
        return 'PARADO'
