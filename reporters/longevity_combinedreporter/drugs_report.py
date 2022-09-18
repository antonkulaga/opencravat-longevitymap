import os

RSID_COL_NAME = "Variant/Haplotypes"
DRUGS_COL_NAME = "Drug(s)"
PHENCAT_COL_NAME = "Phenotype Category"
SIGNIFICANCE_COL_NAME = "Significance"
SENTENCE_COL_NAME = "Sentence"
FREQCASES_COL_NAME = "Allele Of Frequency In Cases"
FREQCONTROLS_COL_NAME = "Allele Of Frequency In Controls"
TYPE_COL_NAME = "Ratio Stat Type"
RATIOSTAT_COL_NAME = "Ratio Stat"


class DrugsReport:
    index = 0
    def init(self, reporter):
        self.parent = reporter


    def data_name(self):
        return "DRUGS"


    def data(self):
        return {"IND":[], "RSID":[], "DRUGS":[], "PHENCAT":[], "SIGNIFICANCE":[],
                "SENTENCE":[], "FREQCASES":[], "FREQCONTROLS":[], "TYPE":[], "EFFECT":[]}


    def setup(self):
        with open(os.path.dirname(__file__)+"/annotation_tab.tsv") as f:
            self.annotation_tab = {}
            header = True
            head = None
            rsid_index = -1
            for line in f:
                if header:
                    head = line.split("\t")
                    rsid_index = head.index(RSID_COL_NAME)
                    self.annotation_tab["header"] = head
                    header = False
                else:
                    parts = line.split("\t")
                    self.annotation_tab[parts[rsid_index]] = parts
            self.head_index_map = {}
            for i, item in enumerate(head):
                self.head_index_map[item] = i


    def process_row(self, row):
        rsid = self.parent.get_value(row, 'dbsnp__rsid')
        item = self.annotation_tab.get(rsid)
        if item is None:
            return

        self.index += 1
        self.parent.data["DRUGS"]["IND"].append(self.index)
        self.parent.data["DRUGS"]["RSID"].append(rsid)
        self.parent.data["DRUGS"]["DRUGS"].append(item[self.head_index_map[DRUGS_COL_NAME]])
        self.parent.data["DRUGS"]["PHENCAT"].append(item[self.head_index_map[PHENCAT_COL_NAME]])
        self.parent.data["DRUGS"]["SIGNIFICANCE"].append(item[self.head_index_map[SIGNIFICANCE_COL_NAME]])
        self.parent.data["DRUGS"]["SENTENCE"].append(item[self.head_index_map[SENTENCE_COL_NAME]])
        freq_in_case = item[self.head_index_map[FREQCASES_COL_NAME]]
        self.parent.data["DRUGS"]["FREQCASES"].append(freq_in_case)
        self.parent.data["DRUGS"]["FREQCONTROLS"].append(item[self.head_index_map[FREQCONTROLS_COL_NAME]])
        self.parent.data["DRUGS"]["TYPE"].append(item[self.head_index_map[TYPE_COL_NAME]])
        effect = float(item[self.head_index_map[RATIOSTAT_COL_NAME]])
        alt = self.parent.get_value(row, 'base__alt_base')
        if freq_in_case != alt:
            effect = round((1/effect)*1000)/1000
        self.parent.data["DRUGS"]["EFFECT"].append(str(effect))


    def end(self):
        pass