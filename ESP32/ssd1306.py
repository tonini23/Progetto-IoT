from micropython import const
import framebuf

# Definizione dei comandi tecnici per il display
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_DIR = const(0xC0)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_OFFSET = const(0xD3)
SET_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)


class SSD1306(framebuf.FrameBuffer):

    def __init__(self, larghezza, altezza, vcc_esterna):
        self.larghezza = larghezza
        self.altezza = altezza
        self.vcc_esterna = vcc_esterna
        self.pagine = self.altezza // 8
        # Creazione della memoria  per i pixel dello schermo
        self.buffer = bytearray(self.pagine * self.larghezza)
        super().__init__(self.buffer, self.larghezza, self.altezza, framebuf.MONO_VLSB)
        self.inizializza_display()

    def inizializza_display(self):
        # Invio dei comandi per accendere e configurare lo schermo
        for cmd in (
            SET_DISP | 0x00,  # Spegne temporaneamente il display
            SET_MEM_ADDR,
            0x00,  # Scrittura orizzontale
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,  
            SET_MUX_RATIO,
            self.altezza - 1,
            SET_COM_DIR | 0x08,  
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.altezza == 32 else 0x12,
            SET_CONTRAST,
            0xFF,  # Contrasto massimo
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.vcc_esterna else 0xF1,
            SET_VCOM_DESEL,
            0x30,  
            SET_CHARGE_PUMP,
            0x10 if self.vcc_esterna else 0x14,
            SET_DISP | 0x01,  # Riaccende il display alla fine
        ):
            self.scrivi_comando(cmd)
        self.fill(0)  # Pulisce lo schermo
        self.mostra() # Aggiorna la schermata

    def spegni(self):
        # Spegne il display
        self.scrivi_comando(SET_DISP | 0x00)

    def accendi(self):
        # Riaccendi il display
        self.scrivi_comando(SET_DISP | 0x01)

    def imposta_contrasto(self, valore):
        # Cambia la luminosità
        self.scrivi_comando(SET_CONTRAST)
        self.scrivi_comando(valore)

    def inverti_colori(self, attiva):
        # Inverte i pixel (da bianco a nero)
        self.scrivi_comando(SET_NORM_INV | (attiva & 1))

    def mostra(self):
        # Invia i dati dalla memoria al display fisico per visualizzarli
        x0 = 0
        x1 = self.larghezza - 1
        if self.larghezza == 64:
            x0 += 2
            x1 += 2
        self.scrivi_comando(SET_COL_ADDR)
        self.scrivi_comando(x0)
        self.scrivi_comando(x1)
        self.scrivi_comando(SET_PAGE_ADDR)
        self.scrivi_comando(0)
        self.scrivi_comando(self.pagine - 1)
        self.scrivi_dati(self.buffer)


class SSD1306_I2C(SSD1306):

    def __init__(self, larghezza, altezza, i2c, indirizzo=0x3C, vcc_esterna=False):
        self.i2c = i2c
        self.indirizzo = indirizzo
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]
        super().__init__(larghezza, altezza, vcc_esterna)

    def scrivi_comando(self, cmd):
        # Invia un comando via I2C
        self.temp[0] = 0x80  
        self.temp[1] = cmd
        self.i2c.writeto(self.indirizzo, self.temp)

    def scrivi_dati(self, buf):
        # Invia i dati dei pixel via I2C
        self.write_list[1] = buf
        self.i2c.writevto(self.indirizzo, self.write_list)