import unittest
import gdbresultparser


class Test(unittest.TestCase):
    def setUp(self):
        self.parser = gdbresultparser.GdbResultParser()

    def tearDown(self):
        pass

    def test1(self):
        self.parser.parse(["""^done"""])

    def test2(self):
        self.parser.parse(["""
=thread-group-added,id="i1"
~"GNU gdb (Ubuntu/Linaro 7.3-0ubuntu2) 7.3-2011.08\n"
~"Copyright (C) 2011 Free Software Foundation, Inc.\n"
~"License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.  Type \"show copying\"\nand \"show warranty\" for details.\n"
~"This GDB was configured as \"x86_64-linux-gnu\".\nFor bug reporting instructions, please see:\n"
~"<http://bugs.launchpad.net/gdb-linaro/>.\n"
        """])

    def test3(self):
        self.parser.parse(["""
        ^done,name="var2",numchild="2",value="[2]",type="int *[2]",thread-id="1",has_more="0"
        """])

    def test4(self):
        self.parser.parse(["""
        ^done,numchild="2",children=[child={name="var2.0",exp="0",numchild="1",value="0x7fffffffe4f8",type="int *",thread-id="1"},child={name="var2.1",exp="1",numchild="1",value="0x400600",type="int *",thread-id="1"}],has_more="0"
        """])

    def test5(self):
        self.parser.parse(["""
        ^done,numchild="2",children=[child={name="var4.public.array",exp="array",numchild="200",value="[200]",type="int [200]",thread-id="1"},child={name="var4.public.num",exp="num",numchild="0",value="1",type="int",thread-id="1"}],has_more="0"
        """])

    def test6(self):
        self.parser.parse(["""
        ^done,stack=[frame={level="0",addr="0x000000000040056f",func="main",file="main.cpp",fullname="/home/rainer/tmp/testprog/bigarray/main.cpp",line="14"}]
        """])

    def test7(self):
        self.parser.parse(["""
        =library-loaded,id="/lib64/ld-linux-x86-64.so.2",target-name="/lib64/ld-linux-x86-64.so.2",host-name="/lib64/ld-linux-x86-64.so.2",symbols-loaded="0",thread-group="i1"
        =library-loaded,id="/usr/lib/x86_64-linux-gnu/libstdc++.so.6",target-name="/usr/lib/x86_64-linux-gnu/libstdc++.so.6",host-name="/usr/lib/x86_64-linux-gnu/libstdc++.so.6",symbols-loaded="0",thread-group="i1"
        =library-loaded,id="/lib/x86_64-linux-gnu/libc.so.6",target-name="/lib/x86_64-linux-gnu/libc.so.6",host-name="/lib/x86_64-linux-gnu/libc.so.6",symbols-loaded="0",thread-group="i1"
        =library-loaded,id="/lib/x86_64-linux-gnu/libm.so.6",target-name="/lib/x86_64-linux-gnu/libm.so.6",host-name="/lib/x86_64-linux-gnu/libm.so.6",symbols-loaded="0",thread-group="i1"
        =library-loaded,id="/lib/x86_64-linux-gnu/libgcc_s.so.1",target-name="/lib/x86_64-linux-gnu/libgcc_s.so.1",host-name="/lib/x86_64-linux-gnu/libgcc_s.so.1",symbols-loaded="0",thread-group="i1"
        *stopped,reason="breakpoint-hit",disp="keep",bkptno="1",frame={addr="0x000000000040056f",func="main",args=[],file="main.cpp",fullname="/home/rainer/tmp/testprog/bigarray/main.cpp",line="14"},thread-id="1",stopped-threads="all",core="2"
        """])

    def test8(self):
        self.parser.parse(["""
        ^done,numchild="2",children=[child={name="var4.public.array",exp="array",numchild="200",value="[200]",type="int [200]",thread-id="1"},child={name="var4.public.num",exp="num",numchild="0",value="1",type="int",thread-id="1"}],has_more="0"
        """])

    def test9(self):
        self.parser.parse(["""
        ^done,numchild="200",children=[child={name="var6.public.array.0",exp="0",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.1",exp="1",numchild="0",value="-4163",type="int",thread-id="1"},child={name="var6.public.array.2",exp="2",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.3",exp="3",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.4",exp="4",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.5",exp="5",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.6",exp="6",numchild="0",value="-134227496",type="int",thread-id="1"},child={name="var6.public.array.7",exp="7",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.8",exp="8",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.9",exp="9",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.10",exp="10",numchild="0",value="-1061158912",type="int",thread-id="1"},child={name="var6.public.array.11",exp="11",numchild="0",value="-1",type="int",thread-id="1"},child={name="var6.public.array.12",exp="12",numchild="0",value="1398145024",type="int",thread-id="1"},child={name="var6.public.array.13",exp="13",numchild="0",value="-4163",type="int",thread-id="1"},child={name="var6.public.array.14",exp="14",numchild="0",value="-136397200",type="int",thread-id="1"},child={name="var6.public.array.15",exp="15",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.16",exp="16",numchild="0",value="-143347756",type="int",thread-id="1"},child={name="var6.public.array.17",exp="17",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.18",exp="18",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.19",exp="19",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.20",exp="20",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.21",exp="21",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.22",exp="22",numchild="0",value="-134224352",type="int",thread-id="1"},child={name="var6.public.array.23",exp="23",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.24",exp="24",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.25",exp="25",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.26",exp="26",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.27",exp="27",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.28",exp="28",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.29",exp="29",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.30",exp="30",numchild="0",value="-136460484",type="int",thread-id="1"},child={name="var6.public.array.31",exp="31",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.32",exp="32",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.33",exp="33",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.34",exp="34",numchild="0",value="-134239816",type="int",thread-id="1"},child={name="var6.public.array.35",exp="35",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.36",exp="36",numchild="0",value="-8208",type="int",thread-id="1"},child={name="var6.public.array.37",exp="37",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.38",exp="38",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.39",exp="39",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.40",exp="40",numchild="0",value="6295120",type="int",thread-id="1"},child={name="var6.public.array.41",exp="41",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.42",exp="42",numchild="0",value="-136423740",type="int",thread-id="1"},child={name="var6.public.array.43",exp="43",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.44",exp="44",numchild="0",value="-134239816",type="int",thread-id="1"},child={name="var6.public.array.45",exp="45",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.46",exp="46",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.47",exp="47",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.48",exp="48",numchild="0",value="6",type="int",thread-id="1"},child={name="var6.public.array.49",exp="49",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.50",exp="50",numchild="0",value="-134395224",type="int",thread-id="1"},child={name="var6.public.array.51",exp="51",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.52",exp="52",numchild="0",value="-1742731663",type="int",thread-id="1"},child={name="var6.public.array.53",exp="53",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.54",exp="54",numchild="0",value="-136421674",type="int",thread-id="1"},child={name="var6.public.array.55",exp="55",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.56",exp="56",numchild="0",value="6",type="int",thread-id="1"},child={name="var6.public.array.57",exp="57",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.58",exp="58",numchild="0",value="49",type="int",thread-id="1"},child={name="var6.public.array.59",exp="59",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.60",exp="60",numchild="0",value="-7328",type="int",thread-id="1"},child={name="var6.public.array.61",exp="61",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.62",exp="62",numchild="0",value="39878681",type="int",thread-id="1"},child={name="var6.public.array.63",exp="63",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.64",exp="64",numchild="0",value="-139615732",type="int",thread-id="1"},child={name="var6.public.array.65",exp="65",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.66",exp="66",numchild="0",value="-139613528",type="int",thread-id="1"},child={name="var6.public.array.67",exp="67",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.68",exp="68",numchild="0",value="-7296",type="int",thread-id="1"},child={name="var6.public.array.69",exp="69",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.70",exp="70",numchild="0",value="-139536776",type="int",thread-id="1"},child={name="var6.public.array.71",exp="71",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.72",exp="72",numchild="0",value="-143431992",type="int",thread-id="1"},child={name="var6.public.array.73",exp="73",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.74",exp="74",numchild="0",value="-143426464",type="int",thread-id="1"},child={name="var6.public.array.75",exp="75",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.76",exp="76",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.77",exp="77",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.78",exp="78",numchild="0",value="-136423740",type="int",thread-id="1"},child={name="var6.public.array.79",exp="79",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.80",exp="80",numchild="0",value="-134241072",type="int",thread-id="1"},child={name="var6.public.array.81",exp="81",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.82",exp="82",numchild="0",value="2",type="int",thread-id="1"},child={name="var6.public.array.83",exp="83",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.84",exp="84",numchild="0",value="6",type="int",thread-id="1"},child={name="var6.public.array.85",exp="85",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.86",exp="86",numchild="0",value="-134395224",type="int",thread-id="1"},child={name="var6.public.array.87",exp="87",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.88",exp="88",numchild="0",value="-163754450",type="int",thread-id="1"},child={name="var6.public.array.89",exp="89",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.90",exp="90",numchild="0",value="-136421674",type="int",thread-id="1"},child={name="var6.public.array.91",exp="91",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.92",exp="92",numchild="0",value="-143374336",type="int",thread-id="1"},child={name="var6.public.array.93",exp="93",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.94",exp="94",numchild="0",value="46",type="int",thread-id="1"},child={name="var6.public.array.95",exp="95",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.96",exp="96",numchild="0",value="-7184",type="int",thread-id="1"},child={name="var6.public.array.97",exp="97",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.98",exp="98",numchild="0",value="64550200",type="int",thread-id="1"},child={name="var6.public.array.99",exp="99",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.100",exp="100",numchild="0",value="-143426964",type="int",thread-id="1"},child={name="var6.public.array.101",exp="101",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.102",exp="102",numchild="0",value="-143426464",type="int",thread-id="1"},child={name="var6.public.array.103",exp="103",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.104",exp="104",numchild="0",value="-134241072",type="int",thread-id="1"},child={name="var6.public.array.105",exp="105",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.106",exp="106",numchild="0",value="-143377336",type="int",thread-id="1"},child={name="var6.public.array.107",exp="107",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.108",exp="108",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.109",exp="109",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.110",exp="110",numchild="0",value="-134394552",type="int",thread-id="1"},child={name="var6.public.array.111",exp="111",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.112",exp="112",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.113",exp="113",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.114",exp="114",numchild="0",value="-134395128",type="int",thread-id="1"},child={name="var6.public.array.115",exp="115",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.116",exp="116",numchild="0",value="-134239816",type="int",thread-id="1"},child={name="var6.public.array.117",exp="117",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.118",exp="118",numchild="0",value="4195187",type="int",thread-id="1"},child={name="var6.public.array.119",exp="119",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.120",exp="120",numchild="0",value="-143374336",type="int",thread-id="1"},child={name="var6.public.array.121",exp="121",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.122",exp="122",numchild="0",value="4195072",type="int",thread-id="1"},child={name="var6.public.array.123",exp="123",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.124",exp="124",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.125",exp="125",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.126",exp="126",numchild="0",value="2047",type="int",thread-id="1"},child={name="var6.public.array.127",exp="127",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.128",exp="128",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.129",exp="129",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.130",exp="130",numchild="0",value="-134224352",type="int",thread-id="1"},child={name="var6.public.array.131",exp="131",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.132",exp="132",numchild="0",value="-7120",type="int",thread-id="1"},child={name="var6.public.array.133",exp="133",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.134",exp="134",numchild="0",value="-163754450",type="int",thread-id="1"},child={name="var6.public.array.135",exp="135",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.136",exp="136",numchild="0",value="-134395128",type="int",thread-id="1"},child={name="var6.public.array.137",exp="137",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.138",exp="138",numchild="0",value="-7080",type="int",thread-id="1"},child={name="var6.public.array.139",exp="139",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.140",exp="140",numchild="0",value="-134225208",type="int",thread-id="1"},child={name="var6.public.array.141",exp="141",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.142",exp="142",numchild="0",value="-136421005",type="int",thread-id="1"},child={name="var6.public.array.143",exp="143",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.144",exp="144",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.145",exp="145",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.146",exp="146",numchild="0",value="-134395128",type="int",thread-id="1"},child={name="var6.public.array.147",exp="147",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.148",exp="148",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.149",exp="149",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.150",exp="150",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.151",exp="151",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.152",exp="152",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.153",exp="153",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.154",exp="154",numchild="0",value="-134225208",type="int",thread-id="1"},child={name="var6.public.array.155",exp="155",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.156",exp="156",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.157",exp="157",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.158",exp="158",numchild="0",value="-134225408",type="int",thread-id="1"},child={name="var6.public.array.159",exp="159",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.160",exp="160",numchild="0",value="-139536776",type="int",thread-id="1"},child={name="var6.public.array.161",exp="161",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.162",exp="162",numchild="0",value="-134241072",type="int",thread-id="1"},child={name="var6.public.array.163",exp="163",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.164",exp="164",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.165",exp="165",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.166",exp="166",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.167",exp="167",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.168",exp="168",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.169",exp="169",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.170",exp="170",numchild="0",value="-134224352",type="int",thread-id="1"},child={name="var6.public.array.171",exp="171",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.172",exp="172",numchild="0",value="-1",type="int",thread-id="1"},child={name="var6.public.array.173",exp="173",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.174",exp="174",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.175",exp="175",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.176",exp="176",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.177",exp="177",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.178",exp="178",numchild="0",value="4195187",type="int",thread-id="1"},child={name="var6.public.array.179",exp="179",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.180",exp="180",numchild="0",value="3081792",type="int",thread-id="1"},child={name="var6.public.array.181",exp="181",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.182",exp="182",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.183",exp="183",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.184",exp="184",numchild="0",value="-136586416",type="int",thread-id="1"},child={name="var6.public.array.185",exp="185",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.186",exp="186",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.187",exp="187",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.188",exp="188",numchild="0",value="-139636736",type="int",thread-id="1"},child={name="var6.public.array.189",exp="189",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.190",exp="190",numchild="0",value="-136405020",type="int",thread-id="1"},child={name="var6.public.array.191",exp="191",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.192",exp="192",numchild="0",value="1",type="int",thread-id="1"},child={name="var6.public.array.193",exp="193",numchild="0",value="32767",type="int",thread-id="1"},child={name="var6.public.array.194",exp="194",numchild="0",value="4195840",type="int",thread-id="1"},child={name="var6.public.array.195",exp="195",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.196",exp="196",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.197",exp="197",numchild="0",value="0",type="int",thread-id="1"},child={name="var6.public.array.198",exp="198",numchild="0",value="4195395",type="int",thread-id="1"},child={name="var6.public.array.199",exp="199",numchild="0",value="0",type="int",thread-id="1"}],has_more="0"
        """])

    def test10(self):
        self.parser.parse(["""
        ^done,changelist=[{name="var17.public.array.1",value="200",in_scope="true",type_changed="false",has_more="0"},{name="var6.public.array.1",value="200",in_scope="true",type_changed="false",has_more="0"}]
        """])

    def test11(self):
        # gdb 6.something uses this incorrect format ("{..}" instead of ("[..]"
        # for lists); we don't support this
        self.assertRaises(Exception, self.parser.parse, ["""
        ^done,files={{file="/System/Library/Frameworks/System.framework/PrivateHeaders/ppc/cpu_capabilities.h"},{file="/System/Library/Frameworks/System.framework/PrivateHeaders/machine/cpu_capabilities.h"},{file="<command line>"},{file="<built-in>"},{file="/SourceCache/Libsystem/Libsystem-88.1.12//"},{file="CommPageSymbols.st"},{file="{standard input}"}}
        """])

    def test12(self):
        self.parser.parse(["""
        ^done,files=[{file="main.cpp",fullname="/home/rainer/tmp/testprog/bigarray/main.cpp"}]
        """])

if __name__ == "__main__":
    unittest.main()
