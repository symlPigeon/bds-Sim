#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: syml
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from hier_B1CCarrierPilot2Vector import hier_B1CCarrierPilot2Vector  # grc-generated hier_block
from hier_B1CDataPilot2Vector import hier_B1CDataPilot2Vector  # grc-generated hier_block
from hier_B1C_hexdata2vec import hier_B1C_hexdata2vec  # grc-generated hier_block
from hier_b1c_boc import hier_b1c_boc  # grc-generated hier_block
import math



from gnuradio import qtgui

class b1c_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "b1c_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 6.138e6 * 4
        self.pilot_sps = pilot_sps = 1.023e6
        self.f_sc_b1c_b = f_sc_b1c_b = 6.138e6
        self.f_sc_b1c_a = f_sc_b1c_a = 1.023e6
        self.data_sps = data_sps = 100

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(1575.42e6, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(32.736e6, 0)
        self.uhd_usrp_sink_0.set_gain(30, 0)
        self.qtgui_freq_sink_x_1_1 = qtgui.freq_sink_f(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            32.736e6, #bw
            "s_b1c_pilot_b", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_1.enable_grid(False)
        self.qtgui_freq_sink_x_1_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_1_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_1_win)
        self.qtgui_freq_sink_x_1_0 = qtgui.freq_sink_f(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            32.736e6, #bw
            "s_b1c_pilot_a", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_1_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_1_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_0_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_f(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            32.736e6, #bw
            "s_b1c_data", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            32.736e6, #bw
            "boc", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.hier_b1c_boc_0 = hier_b1c_boc(
            delay=0,
            f_sc_b1c_a=1.023e6,
            f_sc_b1c_b=(1.023e6 * 6),
        )
        self.hier_B1C_hexdata2vec_0 = hier_B1C_hexdata2vec(
            hex_data='582932151c5cd6ab2c1f012773b096d537821b8452ac19a29f8b5688341ed7b3a6999cef9a038f8b79d2eb322c8b2c57b0408e4d6ef50a40fae709b7d5e1282148899fb0a07891158c6333e8b1b4267b0cd2a160e415141f8ff453716a12c79513fc59536209931454231e3b082e63e190a8e64de29a038f8b39d2eb322d8b2c57b0308e4d6ef40a40fae719b7d5e12c2148899fc0a07891118c6333e891b4267b0bd2a160e415141f8ff253716a12d79513fc58536209930454231e38082e63e1f0a8e64de512244eee71b5c6c91f7b182d54b50733b462544e25abd5867e3f9c',
        )
        self.hier_B1CDataPilot2Vector_0 = hier_B1CDataPilot2Vector(
            oct_pilot='52312612361774421055177170113601623050322416375257170635277424772533443335255741222041471147163617537103660211266274733067525272720402727566064413222661361412415052434637354020065724300061210664606375050270016630172514574423410554364167040107260350404405561743031470450370603730727657360277363026564624527744701264750342317640012206512065352470030220754573125614156650635354444275512415626512750517325135314726667077132020030345521332246611364564475440325542254400463456046620132532667643366545432125226452603034764215013605664544301331724264176233371435532544424056753716377672742607132440012203714041103165615137247113455050144127712713474340535170160232123512305540477643227106543771040132230265115626626226566642356066600420743230437172156037123046462621451740730571742145436042006660734426672644646647311264144550021177432611645427762033214513450544070171352034363516517650230121323511625751307271411020317404500022551606436567774717536720242232553343175544770264257155014232267207501304276341406522645250543232675427666552550046620723462002324433254023362272275106624555053234140040551761666656315351255712136512647302513364222335346126730307251572336044140162535260512604500027714434136265016237652246272641475764075727656157406174122163141437073202202134065610021670274332103442372312570146700164121374606266105060014257260040335746342521302503075066445502260673656402056565253661556364665104067411753707471631163020445037325355423552576243765346171725374702454121447007510171771321042377074506514525626755214063321001413060655147355513527274622731746526543715202154634227506460230436127601271463241554335274247540714045654615076051437132164624575627115517242157603133045444433203330345361461601103310317301364530472172320656574150277355031460536537315737440701500271702502546315537575104543734261745751457457776331575023014264561262362777216571007457372707066773263175526753146130524651237203163021435025140653754112135621625655252203073116163440573351325240767767030054365244127012624745664473647335154156214753560314210256261206572772056741202432660402740413357716241770314227471407612730261014562133672135141001547645442457471162242433643557447377653363641210000533424456132606211513067201435076220437206032303621113517511307125707605065037322466546237646362526725142043112323747705267247200673515540434114364720552711340446176670113262163713770074653300274744775001473456513721065164447152213064077345047516345650611425000372572720672715031132071421470264460547273027275276000521443053516345710516770130642254711134530427645351671400577117172006653170077647634232644073374311016447255027136144161015545673002712732507717626244610214527325236313762315331226760530503707524706445745644423606260102761022370561402730645442303264351121665000042413636653776711755613661212234471751211513715400414564273664235140432067243701471722146077412347756641017201033261202417350277275302432352042146035657142354154566713671133517123240724112536150060737737012526456675011634344670602252553523423564244157653014520561420634602762453125064314657325574632677330707276751700475342777236232435132140620575466377751751457517432167615104575765546315205207472005407011767546765365031460556772054175353026274271065136406746046604403431436516066602661111510664603754212745544723575123134264761450370543153510147015712172566155412631472403724361062031305722163154202547615325317467223172725645556714553030641400426630142557',
        )
        self.hier_B1CCarrierPilot2Vector_0 = hier_B1CCarrierPilot2Vector(
            oct_pilot='06323465052753403277342750714114031226540113163145367153710047454613422163103613301367642770142231617225411216455764244674616375570021736514062506720220264772065323654747274554616465114702116045770125455245052133372535021327352352200076165504435714264451671026626173443111003035231461554053263703332354047476056246434716200425576657062425025206265626464224373017576335063142756365257674465473377044771764073605130664426272737360220112202263661515075645040370336035051361752507121435403272277154702563526443400514632217676260364466116534335563443625576351561445564640530630247601641472217310152317260067764157576336050505042603030057252304444270274353306220320664540262276600227536264436744305657736413302567151622765633656604476712026243677552310572104603437656140672231626404712355262311161770477367051034125516705314722674051124571243625031504037407505442711776024532735675311451674236031204452370532764011261701666554301525173044575567162710357301545422637606340043177626772477147712773237746100163037632215154067560472347355751106745254061553334074324401372650762511024603621734514465735672651203774472115057017601054605236124751244501732271465073455241604507367710774344462325562471013234622730143537616031042750462557736123202473711033536635372234547352066413677535061173611323657220033722320151330260223066561720721111062527500606032105050503663757541377300327462540467422714134037120630650131355114354563755236116355661653443311360323737422631450016113256352071547722726015614247052574364505603660760105135705454336322022440220367672722211330645036701374771107766715311737525363572146305663757406761221313235323025205212307533755210023471613123503717101562666076326501554314625606004446116743233204734511321475611055343700022562567264205652766642505125515240775103442071445313431551727171536265302771320220273052301453674200755763431731121375513424415227434622140772137364066436046342216431517100476547365146346440153224601441470572167726016572505316263051170251114752443616323514772276710672352117714531066305413414501603335352263445732121404565423233254476457027746503635056627016617400376053250351751326360512544230315560320047225422255604254063323170332247033755147543732545462441062630051564430045647035254120350455136206510645447051301616470052370523332273767250710520652777242421775367631353136125145423417021672642014642301121172014413005735710472276457536614140243045071324531331420251003417377471133246413020400225546144107025535010024237260477705752327341415727410116202141733033166415146011436721674331423005372424033772273276445245547134011637752274002425144677421102132060471743763205025606616656411033237667035425334225751576564412255211746624625676206242137110463373144223721051411756514515476212651204565766276510732506703557713302205655615416502413177076344141321022107754462505000751277716200723466452445753351377300505372403106330756135706201462605563303336061011620207536606073531276437744153710500202726503420461466510004103205453322347773607002250106332324532342443050060615727645751344236736403204601362122031054601055356103607106462521723272317572776105053775254124234253577351333124371240345616032243446454225411722644270120652703456440304566240315142045146465337067462677303451330363133140650416651106513440130166630310465224171532276270253241770007615603515642717025477503645744653313106564406121336447151272733016024607206431542324637621271354235751374627131617045274622250',
            oct_subpilot='566553056162733755315542720022654036301050004225023473732661563351607337174461423010755517201331270017604467516570737665514523761171125144324162000063056502310372052001654406625406114111070625151716005765132035420414717535432660242261016555314562005132451615766050460021773715254357707753503053434767310144135244046672165267375322203105220455177057152375244736217274716727433003507066167241630366123525722001745760342744577707340203563617441354202717734765564701307550641570013733011657510324707664033025335121634534512103746326317604245165163424566520660133707126045753440667640075413055706407135537',
        )
        self.blocks_repeat_2 = blocks.repeat(gr.sizeof_char*1, (int(samp_rate / data_sps)))
        self.blocks_repeat_1 = blocks.repeat(gr.sizeof_char*1, (int(samp_rate / pilot_sps)))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, (int(samp_rate / pilot_sps)))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_repeat_0, 0), (self.hier_b1c_boc_0, 2))
        self.connect((self.blocks_repeat_1, 0), (self.hier_b1c_boc_0, 1))
        self.connect((self.blocks_repeat_2, 0), (self.hier_b1c_boc_0, 0))
        self.connect((self.hier_B1CCarrierPilot2Vector_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.hier_B1CDataPilot2Vector_0, 0), (self.blocks_repeat_1, 0))
        self.connect((self.hier_B1C_hexdata2vec_0, 0), (self.blocks_repeat_2, 0))
        self.connect((self.hier_b1c_boc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.hier_b1c_boc_0, 1), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.hier_b1c_boc_0, 3), (self.qtgui_freq_sink_x_1_0, 0))
        self.connect((self.hier_b1c_boc_0, 2), (self.qtgui_freq_sink_x_1_1, 0))
        self.connect((self.hier_b1c_boc_0, 0), (self.uhd_usrp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "b1c_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate / self.pilot_sps)))
        self.blocks_repeat_1.set_interpolation((int(self.samp_rate / self.pilot_sps)))
        self.blocks_repeat_2.set_interpolation((int(self.samp_rate / self.data_sps)))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_pilot_sps(self):
        return self.pilot_sps

    def set_pilot_sps(self, pilot_sps):
        self.pilot_sps = pilot_sps
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate / self.pilot_sps)))
        self.blocks_repeat_1.set_interpolation((int(self.samp_rate / self.pilot_sps)))

    def get_f_sc_b1c_b(self):
        return self.f_sc_b1c_b

    def set_f_sc_b1c_b(self, f_sc_b1c_b):
        self.f_sc_b1c_b = f_sc_b1c_b

    def get_f_sc_b1c_a(self):
        return self.f_sc_b1c_a

    def set_f_sc_b1c_a(self, f_sc_b1c_a):
        self.f_sc_b1c_a = f_sc_b1c_a

    def get_data_sps(self):
        return self.data_sps

    def set_data_sps(self, data_sps):
        self.data_sps = data_sps
        self.blocks_repeat_2.set_interpolation((int(self.samp_rate / self.data_sps)))




def main(top_block_cls=b1c_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
