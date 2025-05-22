#!/usr/bin/env python

# Plotting JECs from txt files
# 09042024/S.Lehti
usage_ = "Usage: %prog inputfile(s) [options]"

import textwrap

description_ = textwrap.dedent("""\
Plotting JECs from txt files.
Doesn't require CMSSW env or scientific linux.
    Make the ref and target jec-txt-files with:
    cmsRun jescDBToTxtConverter_cfg.py gt=150X_dataRun3_HLT_JME_Target_w18_v2 onlyHLT=True
    cmsRun jescDBToTxtConverter_cfg.py gt=150X_dataRun3_HLT_v1 onlyHLT=True
""")

import os,sys,re
import array

import ROOT

from optparse import OptionParser, OptionGroup, IndentedHelpFormatter

endings = [".png",".pdf",".C"]

class PreserveNewlinesFormatter(IndentedHelpFormatter):
    def format_description(self, description):
        return description + "\n"

def usage():
    parser.print_help()
    sys.exit()

class JEC:
    def __init__(self,filename):
        self.data = []

        print("JEC",filename)
        fIN = open(filename)
        self.filename = filename.removesuffix(".txt")
        firstline = fIN.readline()
        firstline = firstline.replace('{','')
        firstline = firstline.replace('}','')
        firstline = firstline.split()
        nVariations = int(firstline[0])
        self.variations = firstline[1:][:nVariations]
        nVariables = int(firstline[1+nVariations])
        self.variables = firstline[1+nVariations+1:][:nVariables]

        self.expression = firstline[1+nVariations+1+nVariables]

        self.name = firstline[-1]

        for line in fIN:
            dataline_str = " ".join(line.split())
            if len(dataline_str) == 0:
                continue

            dataline_str = dataline_str.split()
            dataline_float = [float(string) for string in dataline_str]
            self.data.append(dataline_float)

    def getCorrection(self,JetPt,JetEta,JetPhi,JetA,Rho):
        dataline = []
        for d in self.data:
            if len(self.variations) == 1:
                if d[0] <= JetEta and JetEta <= d[1]:
                    dataline = d
                    break
            if len(self.variations) == 2:
                if d[0] <= JetEta and JetEta <= d[1] and d[2] <= JetPhi and JetPhi <= d[3]:
                    dataline = d
                    break

        if len(dataline) == 0:
            return None

        params = dataline[-int(dataline[2*len(self.variations)]-2*len(self.variables)):]
        ranges = []
        for i in range(len(self.variables)):
            ranges.append(dataline[2*len(self.variations)+1+2*i:2*len(self.variations)+1+2*i+2])

        if len(self.variables) == 1:
            func = ROOT.TF1("func",self.expression,ranges[0][0],ranges[0][1])
            for i,p in enumerate(params):
                func.SetParameter(i,p)
            x = JetPt
            return func.Eval(JetPt)
        if len(self.variables) == 3:
            func = ROOT.TF3("func",self.expression,ranges[0][0],ranges[0][1],ranges[1][0],ranges[1][1],ranges[2][0],ranges[2][1])
            for i,p in enumerate(params):
                func.SetParameter(i,p)

            x,y,z = assign_variables(self.variables, JetPt, JetA, Rho)

            #import math
            #print("should",max(0.0001,params[0]+(params[1]/(pow(math.log10(x),2)+params[2]))+(params[3]*math.exp(-(params[4]*((math.log10(x)-params[5])*(math.log10(x)-params[5])))))+(params[6]*math.exp(-(params[7]*((math.log10(x)-params[8])*(math.log10(x)-params[8])))))))
            #print("value",func.Eval(JetPt))
            #print("should",max(0.0001,1-(z/y)*(params[0]+(params[1]*(x))*(1+params[2]*math.log(y)))))
            #print("value",func.Eval(Rho,JetPt,JetA))
            #print("should",1-params[0]*y*(z-params[1])/x)
            #print("value",func.Eval(JetPt,JetA,Rho))
            #print("formula",func.GetFormula().GetExpFormula(),func.GetFormula().GetParameter(0),func.GetFormula().GetParameter(1),func.GetFormula().GetParameter(2))
            return func.Eval(x,y,z)

        return 1.0

def assign_variables(variables, JetPt, JetA, Rho):
    x = y = z = None
    for i, var in enumerate(variables):
        if var == 'JetPt':
            if i == 0:
                x = JetPt
            elif i == 1:
                y = JetPt
            else:
                z = JetPt
        elif var == 'JetA':
            if i == 0:
                x = JetA
            elif i == 1:
                y = JetA
            else:
                z = JetA
        elif var == 'Rho':
            if i == 0:
                x = Rho
            elif i == 1:
                y = Rho
            else:
                z = Rho
    return x, y, z

def plot(x,y,xlabel,ylable,filename,opts,customtext=""):

    ratioPlot = opts.ratio

    base_colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kMagenta, ROOT.kTeal, ROOT.kPink, ROOT.kAzure, ROOT.kCyan, ROOT.kGreen]
    num_shades = 4
    colors = []
    for color in base_colors:
        if color == ROOT.kBlack:
            colors.append(color)
        else:
            for i in range(num_shades):
                colors.append(color + i)

    base_linestyles = [1, 2, 3, 4, 5]  # esim. solid, dashed, dotted, dash-dotted
    num_linestyles = len(base_linestyles)
    linestyles = [base_linestyles[i % num_linestyles] for i in range(len(colors))]

    canvas = ROOT.TCanvas("canvas","",500,500)
    canvas.cd()

    if ratioPlot:
        a1 = 0.01
        b1 = 0.33
        a2 = 0.99
        b2 = 0.99
        graphpad = ROOT.TPad("graphpad","graphpad",a1,b1,a2,b2)
        graphpad.SetTopMargin(0.04)
        graphpad.SetRightMargin(0.04)
        graphpad.SetLeftMargin(0.14)
        graphpad.SetBottomMargin(0)
        if opts.plot_type == 'pt':
            graphpad.SetLogx()
        graphpad.Draw()
        graphpad.cd()
    else:
        canvas.SetTopMargin(0.04)
        canvas.SetRightMargin(0.04)
        canvas.SetLeftMargin(0.14)
        canvas.SetBottomMargin(0.14)
        if opts.plot_type == 'pt':
            canvas.SetLogx()

    graphFrame = ROOT.TH2F("frame","",len(x),min(x),max(x),2,0,3)
    graphFrame.SetStats(0)
    graphFrame.GetXaxis().SetTitle(xlabel)
    graphFrame.GetXaxis().SetTitleOffset(1.2)
    graphFrame.GetXaxis().SetTitleSize(0.05)
    graphFrame.GetYaxis().SetTitleSize(0.05)
    graphFrame.GetYaxis().SetTitleOffset(1.2)
    graphFrame.GetYaxis().SetTitle(ylable)
    graphFrame.Draw()

    if len(customtext) > 0:
        text = ROOT.TText(0.15,0.97,customtext)
        text.SetNDC(True)
        text.SetTextSize(0.02)
        text.Draw()

    jec_re = re.compile(r"(?P<jec>\S+)_(?P<level>L\w+)_(?P<jet>\w+)\.txt")

    legendtitle = "Empty Title"
    filetitle = ""
    legendgraphs = {}
    y_reference = None
    y_ratios = {}

    graph = {}
    for i,key in enumerate(y.keys()):
        x_values = array.array('d',x)
        y_values = array.array('d',y[key])
        if y_reference == None:
            y_reference = y_values
        else:
            gtr1 = False
            ratios = []
            for j in reversed(range(len(y_reference))):
                ratio = y_values[j]/y_reference[j]
                if y_values[j] < 0.0002:
                    ratio = y_values[j]
                if y_reference[j] < 0.0002 and gtr1:
                    ratio = 999
                if ratio > 1:
                    gtr1 = True
                else:
                    gtr1 = False
                ratios.append(ratio)
            ratios = list(reversed(ratios))
            y_ratios[key] = ratios

        if len(y_values) == 0:
            continue

        graph[i] = ROOT.TGraph(len(x),x_values,y_values)
        graph[i].SetName("graph%s"%i)
        graph[i].SetMarkerColor(colors[i])
        graph[i].SetLineColor(colors[i])
        graph[i].SetLineStyle(linestyles[i])
        graph[i].SetLineWidth(2)
        graph[i].Draw("LSAME")

        corrname = "NamelessJEC"
        match = jec_re.search(key)
        if match:
            corrname = match.group("jec")
            legendtitle = match.group("level")+' '+match.group("jet")
            filetitle = legendtitle.replace(' ','_')
        else:
            legendtitle = ""
            corrname = key
        legendgraphs[corrname] = graph[i]

    legend_lower_y = 0.96 - max(0.2,len(graph)*0.03)
    legend = ROOT.TLegend(0.7,legend_lower_y,0.96,0.96)
    if len(legendtitle) > 0:
        legend.SetHeader(legendtitle,"C")
    for key in legendgraphs.keys():
        legend.AddEntry(legendgraphs[key],key)
    legend.Draw()

    canvas.cd()

    if ratioPlot:
        a1 = 0.01
        b1 = 0.01
        a2 = 0.99
        b2 = 0.33
        ratiopad = ROOT.TPad("ratiopad","",a1,b1,a2,b2)
        ratiopad.SetTopMargin(0)
        ratiopad.SetRightMargin(0.04)
        ratiopad.SetLeftMargin(0.14)
        ratiopad.SetBottomMargin(0.3)
        ratiopad.SetFrameBorderMode(0)
        if opts.plot_type == 'pt':
            ratiopad.SetLogx()
        ratiopad.Draw()
        ratiopad.cd()
        ratioFrame = ROOT.TH2F("rframe","",2,graphFrame.GetXaxis().GetBinLowEdge(1),graphFrame.GetXaxis().GetBinLowEdge(graphFrame.GetNbinsX()+1),2,0.9,1.1)
        ratioFrame.SetStats(0)
        ratioFrame.GetXaxis().SetTitle(xlabel)
        titlescale = 2
        ratioFrame.GetXaxis().SetTitleSize(titlescale*graphFrame.GetXaxis().GetTitleSize())
        ratioFrame.GetXaxis().SetLabelSize(titlescale*graphFrame.GetXaxis().GetLabelSize())
        ratioFrame.GetYaxis().SetTitleSize(titlescale*graphFrame.GetYaxis().GetTitleSize())
        ratioFrame.GetYaxis().SetLabelSize(titlescale*graphFrame.GetYaxis().GetLabelSize())
        ratioFrame.GetYaxis().SetTitleOffset(0.65)
        ratioFrame.GetYaxis().SetTitle("Ratio  ")
        ratioFrame.Draw()

        line = ROOT.TLine(min(x),1,max(x),1)
        line.SetLineColor(ROOT.kRed)
        line.SetLineStyle(2)
        line.Draw()
    
        for key in y_ratios.keys():
            x_values = array.array('d',x)
            y_values = array.array('d',y_ratios[key])
            graphr = ROOT.TGraph(len(x),x_values,y_values)
            graphr.SetName(key)
            graphr.Draw("LSAME")

    if len(filetitle) > 0:
        filename += '_' + filetitle

    for ending in endings:
        canvas.SaveAs(filename+ending)


def main(opts, args):

    if len(args) == 0:
        usage()

    correctionfiles = []
    for arg in args:
        if os.path.isfile(arg):
            correctionfiles.append(arg)

    print("Files:",correctionfiles)

    x = []
    y = {}

    phi = 0
    jetA = 2#0.5 # A=0.5 for AK4 and A=2 for AK8
    rho = 30

    if opts.plot_type == 'pt':
        ptrange = range(20,1000)

        binseta = [-5.191, -4.889, -4.716, -4.538, -4.363, -4.191, -4.013, -3.839, -3.664, -3.489,
           -3.314, -3.139, -2.964, -2.853, -2.650, -2.500, -2.322, -2.172, -2.043, -1.930,
           -1.830, -1.740, -1.653, -1.566, -1.479, -1.392, -1.305, -1.218, -1.131, -1.044,
           -0.957, -0.879, -0.783, -0.696, -0.609, -0.522, -0.435, -0.348, -0.261, -0.174,
           -0.087,  0.000,  0.087,  0.174,  0.261,  0.348,  0.435,  0.522,  0.609,  0.696,
            0.783,  0.879,  0.957,  1.044,  1.131,  1.218,  1.305,  1.392,  1.479,  1.566,
            1.653,  1.740,  1.830,  1.930,  2.043,  2.172,  2.322,  2.500,  2.650,  2.853,
            2.964,  3.139,  3.314,  3.489,  3.664,  3.839,  4.013,  4.191,  4.363,  4.538,
            4.716,  4.889,  5.191]

        centers = [(binseta[i] + binseta[i+1])/2 for i in range(len(binseta)-1)]
        abs_centers = [abs(c) for c in centers]
        etarange = list(dict.fromkeys(abs_centers))

        if opts.barrel:
            etarange = [x for x in etarange if x <= 1.566]
        if opts.inner_endcap:
            etarange = [x for x in etarange if 1.566 <= x <= 2.5]
        if opts.outer_endcap:
            etarange = [x for x in etarange if 2.5 <= x <= 3.0]
        if opts.hf:
            etarange = [x for x in etarange if x >= 3.0]

        #print("eta range %s-%s"%(min(etarange),max(etarange)))
        #print("eta range",etarange)
        #etarange = [5.00, 4.8025, 4.627000000000001, 4.4505, 4.277, 4.102, 3.926, 3.7515, 3.5765000000000002, 3.4015, 3.2264999999999997, 3.0515]
        #etarange = [5.191, 4.8025]
        s_etarange = "%.1f_%.1f"%(min(etarange),max(etarange))

        #etarange = [0, 1.3, 2, 2.7, 3.5, 4, 4.5, 5]
        #etarange = [4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5]

        if opts.same:
            #etastr = "eta%s"%eta
            #x = []
            fname = ""
            for eta in etarange:
                etastr = "eta%.1f"%eta
                etastr = etastr.replace('.','p')
                #etatext = "Jet eta = %s"%eta
                jec = JEC(correctionfiles[0])
                text = correctionfiles[0]
                x = []
                y[etastr] = []
                for pt in ptrange:
                    corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                    if not corr == None:
                        x.append(pt)
                        y[etastr].append(corr)
                fname = jec.filename
            fname = "jecs_pt_"+fname
            plot(x,y,"Jet p_{T} (GeV)","JEC",fname+"_etas%s"%s_etarange,opts,text)
        else:
            for eta in etarange:
                etastr = "eta%s"%eta
                etastr = etastr.replace('.','p')
                etatext = "Jet eta = %s"%eta
                for fIN in correctionfiles:
                    jec = JEC(fIN)
                    x = []
                    y[fIN] = []
                    for pt in ptrange:
                        corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                        x.append(pt)
                        y[fIN].append(corr)
            plot(x,y,"Jet p_{T} (GeV)","JEC","jecs_pt_"+etastr,opts,etatext)

    if opts.plot_type == 'eta':
        etarange = list(map(lambda x: x/100.0, range(-500, 501)))
        ptrange = [30, 100, 300, 1000]
        s_ptrange = "%s_%s"%(min(ptrange),max(ptrange))

        if opts.same:
            fname = ""
            for pt in ptrange:
                ptstr = "pt%s"%pt

                jec = JEC(correctionfiles[0])
                text = correctionfiles[0]
                x = []
                y[ptstr] = []
                for eta in etarange:
                    corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                    if not corr == None:
                        x.append(eta)
                        y[ptstr].append(corr)
                fname = jec.filename
            fname = "jecs_eta_"+fname
            plot(x,y,"Jet eta","JEC",fname+"_pts%s"%s_ptrange,opts,text)
        else:
            for pt in ptrange:
                ptstr = "pt%s"%pt
                pttext = "Jet pt = %s GeV"%pt
                for fIN in correctionfiles:
                    jec = JEC(fIN)
                    x = []
                    y[fIN] = []
                    for eta in etarange:
                        corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                        x.append(eta)
                        y[fIN].append(corr)
                plot(x,y,"Jet eta","JEC","jecs_eta_"+ptstr,opts,pttext)

if __name__=="__main__":

    parser = OptionParser(usage=usage_, description=description_, formatter=PreserveNewlinesFormatter())
    group = OptionGroup(parser, "Plot Options", "Choose one of --pt or --eta")
    group.add_option("--pt", dest="plot_type", action="store_const", const="pt",
                     help="Plot as a function of JetPt [default]")
    group.add_option("--eta", dest="plot_type", action="store_const", const="eta",
                     help="Plot as a function of JetEta")
    parser.add_option_group(group)
    parser.set_defaults(plot_type="pt")
    parser.add_option("-b","--barrel", dest="barrel", default=False, action="store_true",
                      help="Plot barrel only [default: False]")
    parser.add_option("-i","--inner_endcap", dest="inner_endcap", default=False, action="store_true",
                      help="Plot inner endcal only [default: False]")
    parser.add_option("-o","--outer_endcap", dest="outer_endcap", default=False, action="store_true",
                      help="Plot outer endcap only [default: False]")
    parser.add_option("-f","--hf", dest="hf", default=False, action="store_true",
                      help="Plot hf only [default: False]")
    parser.add_option("-s", "--same", dest="same", default=False, action="store_true",
                      help="Plot all in the same canvas [default: False]")
    parser.add_option("-r", "--ratio", dest="ratio", default=False, action="store_true",
                      help="Plot ratio [default: False]")

    (opts, args) = parser.parse_args()

    main(opts, args)
