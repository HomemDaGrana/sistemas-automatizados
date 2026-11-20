"""Executar: python A3/testar_modelo.py. Resultados de modelo, sem execução de CLP."""
import csv
import unittest
from pathlib import Path
from modelo_tanque import Entradas, Tanque

class RegrasTanque(unittest.TestCase):
    def pronto(self, minimo=False, maximo=False):
        t,e=Tanque(),Entradas(minimo=minimo,maximo=maximo)
        t.passo(e,3.0)
        return t,e
    def enchendo(self):
        t,e=self.pronto();e.start=True;t.passo(e,0)
        e.retorno=True;t.passo(e,0)
        return t,e
    def test_01_energizacao_parada(self):
        t=Tanque();self.assertFalse(t.comando);self.assertFalse(t.auto)
    def test_02_start_antes_da_prontidao_nao_fica_pendente(self):
        t,e=Tanque(),Entradas(start=True);t.passo(e,1);t.passo(e,2)
        self.assertTrue(t.pronto);self.assertFalse(t.auto)
    def test_03_start_depois_da_prontidao(self):
        t,e=self.pronto();e.start=True;t.passo(e,0);self.assertTrue(t.comando)
    def test_04_histerese_ao_cobrir_minimo(self):
        t,e=self.enchendo();e.minimo=True;t.passo(e,1);self.assertTrue(t.comando)
    def test_05_maximo_para_e_conta_uma_vez(self):
        t,e=self.enchendo();e.minimo=e.maximo=True;t.passo(e,0)
        self.assertFalse(t.comando);self.assertEqual(t.ciclos,1)
        e.retorno=False;t.passo(e,5);self.assertEqual(t.ciclos,1)
    def test_06_nao_inicia_entre_minimo_e_maximo(self):
        t,e=self.pronto(minimo=True);e.start=True;t.passo(e,0)
        self.assertTrue(t.auto);self.assertFalse(t.comando)
    def test_07_reinicia_quando_minimo_seca(self):
        t,e=self.pronto(minimo=True);e.start=True;t.passo(e,0)
        e.minimo=False;t.passo(e,0);self.assertTrue(t.comando)
    def test_08_stop_prevalece(self):
        t,e=self.enchendo();e.stop_ok=False;t.passo(e,0)
        self.assertFalse(t.auto);self.assertFalse(t.comando)
    def test_09_emergencia_memorizada(self):
        t,e=self.enchendo();e.emg_ok=False;t.passo(e,0)
        self.assertIn('EMERGENCIA',t.falhas);self.assertFalse(t.comando)
        e.emg_ok=True;e.retorno=False;t.passo(e,3);self.assertFalse(t.auto)
    def test_10_alto_alto_memorizado(self):
        t,e=self.enchendo();e.minimo=e.maximo=e.hh=True;t.passo(e,0)
        self.assertIn('ALTO_ALTO',t.falhas);self.assertFalse(t.comando)
    def test_11_sensores_incoerentes(self):
        t=Tanque();t.passo(Entradas(maximo=True),0)
        self.assertIn('SENSORES_INCOERENTES',t.falhas)
    def test_12_sobrecarga(self):
        t,e=self.enchendo();e.ol_ok=False;t.passo(e,0)
        self.assertIn('SOBRECARGA',t.falhas);self.assertFalse(t.comando)
    def test_13_fonte_sem_agua(self):
        t,e=self.enchendo();e.fonte_ok=False;t.passo(e,0)
        self.assertIn('SEM_AGUA_NA_FONTE',t.falhas);self.assertFalse(t.comando)
    def test_14_timeout_enchimento(self):
        t,e=self.enchendo();t.passo(e,29.9);self.assertTrue(t.comando)
        t.passo(e,.1);self.assertIn('TEMPO_MAXIMO',t.falhas);self.assertFalse(t.comando)
    def test_15_retorno_atrasado_menos_de_2s(self):
        t,e=self.pronto();e.start=True;t.passo(e,0);t.passo(e,1.9)
        self.assertFalse(t.falhas);e.retorno=True;t.passo(e,.1);self.assertFalse(t.falhas)
    def test_16_retorno_nao_liga(self):
        t,e=self.pronto();e.start=True;t.passo(e,0);t.passo(e,2)
        self.assertIn('RETORNO_DIVERGENTE',t.falhas);self.assertFalse(t.comando)
    def test_17_retorno_nao_desliga(self):
        t,e=self.enchendo();e.stop_ok=False;t.passo(e,2)
        self.assertIn('RETORNO_DIVERGENTE',t.falhas)
    def test_18_reset_nao_reparte(self):
        t,e=self.enchendo();e.emg_ok=False;t.passo(e,0)
        e.emg_ok=True;e.start=False;e.retorno=False;e.reset=True;t.passo(e,0)
        self.assertFalse(t.falhas);self.assertFalse(t.auto)
        e.reset=False;t.passo(e,3);self.assertFalse(t.auto)
        e.start=True;t.passo(e,0);self.assertTrue(t.auto)
    def test_19_reset_com_start_mantido_recusado(self):
        t,e=self.enchendo();e.emg_ok=False;t.passo(e,0)
        e.emg_ok=True;e.retorno=False;e.reset=True;t.passo(e,0)
        self.assertTrue(t.falhas)
    def test_20_reset_com_hh_ativo_recusado(self):
        t,e=self.enchendo();e.minimo=e.maximo=e.hh=True;e.start=False;e.retorno=False
        t.passo(e,0);e.reset=True;t.passo(e,0);self.assertTrue(t.falhas)
    def test_21_start_mantido_apos_stop_nao_reparte(self):
        t,e=self.enchendo();e.stop_ok=False;e.retorno=False;t.passo(e,0)
        e.stop_ok=True;t.passo(e,3);self.assertFalse(t.auto)
    def test_22_power_cycle_nao_retem_habilitacao(self):
        t,e=self.enchendo();self.assertTrue(t.comando)
        t=Tanque();self.assertFalse(t.auto);self.assertEqual(t.ciclos,0)
    def test_23_maximo_no_limite_vence_timeout(self):
        t,e=self.enchendo();t.passo(e,29.9)
        e.minimo=e.maximo=True;t.passo(e,.1)
        self.assertNotIn('TEMPO_MAXIMO',t.falhas);self.assertEqual(t.ciclos,1)
    def test_24_reset_com_retorno_ativo_recusado(self):
        t,e=self.enchendo();e.emg_ok=False;t.passo(e,0)
        e.emg_ok=True;e.start=False;e.reset=True;t.passo(e,0);self.assertTrue(t.falhas)

class Registro(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.rows=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.rows.append([test._testMethodName,'PASSOU','Modelo Python; tempo virtual; não é resultado de CLP'])
    def addFailure(self,test,err):
        super().addFailure(test,err);self.rows.append([test._testMethodName,'FALHOU','Ver saída do teste'])
    def addError(self,test,err):
        super().addError(test,err);self.rows.append([test._testMethodName,'ERRO','Ver saída do teste'])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(RegrasTanque)
    result=unittest.TextTestRunner(verbosity=2,resultclass=Registro).run(suite)
    target=Path(__file__).resolve().parent/'testes-modelo.csv'
    with target.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['Caso','Resultado','Método']);w.writerows(result.rows)
    raise SystemExit(0 if result.wasSuccessful() else 1)
