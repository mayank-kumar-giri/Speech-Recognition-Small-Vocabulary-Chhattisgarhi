import speech_recognition as sr
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
import time
import os
from dtw import *
import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import copy
from sklearn.externals import joblib
from winsound import *

reply = 0
entries = {}
textbs = {}
textpops = ""
test_files = []
current_test = ""
cg_dirname = ""
flag_audio_pop = 0

def language_selection_window(a):
    global reply
    e = entries["mic"]
    reply = int(e.get())
    print(reply)
    def enghin(a):
        # global entries
        # print(entries)
        # e = entries["mic"]
        # rep = int(e.get())
        # print(rep)
        global reply
        rep = reply
        print(rep)
        mic_list = sr.Microphone.list_microphone_names()
        j = 1
        mic_name = ""
        sample_rate = 48000
        chunk_size = 2048
        for i, microphone_name in enumerate(mic_list):
            # print(j,microphone_name)
            if j == rep:
                mic_name = microphone_name
                # print("MIC",mic_name)
            j += 1
        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()

        for i, microphone_name in enumerate(mic_list):

            if microphone_name == mic_name:
                device_id = i
        # print("HELL",device_id)

        def exitf(a):
            root.destroy()

        def status_popup():
            global textpops
            savp = Tk()
            savp.iconbitmap('wait.ico')
            savp.wm_title("Recognition in progress...")
            # Label(savp, text="Please wait...").grid(row=1, column=0, sticky="ew")
            prog = Text(savp, height=10, width=40, bd=5, font=("Times", 20))
            prog.grid(row=2, columnspan=3, sticky="ew")
            # print("txtpps - ", textpops)
            prog.insert(INSERT, "           Recognition in progress, Please wait!    \n")
            prog.insert(INSERT, "                                 Loading!    \n")
            start = time.time()
            while not textpops:
                if (time.time() - start) > 5:
                    break
                prog.insert(INSERT, ".")
                savp.update_idletasks()
                savp.update()
            textpops = ""

        def speakeng(a):
            with sr.Microphone(device_index=device_id, sample_rate=sample_rate, chunk_size=chunk_size) as source:
                # Adjusting noise level
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                global textpops
                t1 = threading.Thread(target=status_popup)
                t1.start()
                try:
                    text = r.recognize_google(audio, language='en-IN')
                    textpops = text
                    # print("Speakeng - ",textpops)
                    text = text + "\n"
                    eng.insert(INSERT, text)
                except sr.UnknownValueError:
                    text = "\n---\nGoogle Speech Recognition could not understand audio\n---\n"
                    eng.insert(INSERT, text)
                except sr.RequestError as e:
                    eng.insert(INSERT, "---")
                    eng.insert(INSERT,
                               "Could not request results from Google Speech Recognition service; {0}".format(e))
                    eng.insert(INSERT, "---")
                t1.join()

                # print("\nt1 still alive - ", t1.is_alive())

        def speakhin(a):
            with sr.Microphone(device_index=device_id, sample_rate=sample_rate, chunk_size=chunk_size) as source:
                # Adjusting noise level
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                global textpops
                t1 = threading.Thread(target=status_popup)
                t1.start()
                try:
                    text = r.recognize_google(audio, language='hi-IN')
                    textpops = text
                    # print("Speakhin - ", textpops)
                    text = text + "\n"
                    hin.insert(INSERT, text)
                except sr.UnknownValueError:
                    text = "\n---\nGoogle Speech Recognition could not understand audio\n---\n"
                    hin.insert(INSERT, text)
                except sr.RequestError as e:
                    hin.insert(INSERT, "---")
                    hin.insert(INSERT,
                               "Could not request results from Google Speech Recognition service; {0}".format(e))
                    hin.insert(INSERT, "---")
                t1.join()
                # print("\nt1 still alive - ", t1.is_alive())

        def cleareng(a):
            eng.delete(1.0, END)

        def clearhin(a):
            hin.delete(1.0, END)

        def saveeng(a):
            location = ""

            def browse(a):
                x = filedialog.askdirectory()
                e = entries["save_file_location"]
                e.insert(0, x)
                location = x

            def savv(a):
                e = entries["save_file_location"]
                location = str(e.get())
                e = entries["save_file_name"]
                name = str(e.get())
                input = eng.get("1.0", 'end-1c')
                # print(name)
                loc = location + "/" + name + ".txt"
                # print("\nFinal loc\n", loc)
                f = open(loc, 'w')
                f.write(input)
                f.close()
                sav.destroy()

            sav = Tk()
            sav.iconbitmap('save.ico')
            sav.wm_title("Save English Transcript")
            Label(sav, text="Enter the file name you want: ").grid(row=0, column=0, sticky=W)
            e = Entry(sav, width=50)
            e.grid(row=1, columnspan=2, sticky="ew")
            entries["save_file_name"] = e
            Label(sav, text="Choose the location to save at: ").grid(row=2, column=0, sticky=W)
            folentry = Entry(sav, width=77)
            folentry.grid(row=3, column=0, sticky="ew")
            entries["save_file_location"] = folentry
            ch = Button(sav, text="Browse")
            ch.bind("<Button-1>", browse)
            ch.grid(row=3, column=1, sticky="ew")
            ttk.Separator(sav).grid(row=4, pady=2, padx=2, columnspan=3, sticky="ew")
            ent = Button(sav, text="Save", width=11)
            ent.bind("<Button-1>", savv)
            ent.grid(row=5, column=1, sticky="ew")
            sav.mainloop()

        def savehin(a):
            location = ""

            def browse(a):
                x = filedialog.askdirectory()
                e = entries["save_file_location"]
                e.insert(0, x)
                location = x

            def savv(a):
                e = entries["save_file_location"]
                location = str(e.get())
                e = entries["save_file_name"]
                name = str(e.get())
                input = hin.get("1.0", 'end-1c')
                # print(name)
                loc = location + "/" + name + ".txt"
                # print("\nFinal loc\n", loc)
                f = open(loc, 'w', encoding="utf-8")
                f.write(input)
                f.close()
                sav.destroy()

            sav = Tk()
            sav.iconbitmap('save.ico')
            sav.wm_title("Save Hindi Transcript")
            Label(sav, text="Enter the file name you want: ").grid(row=0, column=0, sticky=W)
            e = Entry(sav, width=50)
            e.grid(row=1, columnspan=2, sticky="ew")
            entries["save_file_name"] = e
            Label(sav, text="Choose the location to save at: ").grid(row=2, column=0, sticky=W)
            folentry = Entry(sav, width=77)
            folentry.grid(row=3, column=0, sticky="ew")
            entries["save_file_location"] = folentry
            ch = Button(sav, text="Browse")
            ch.bind("<Button-1>", browse)
            ch.grid(row=3, column=1, sticky="ew")
            ttk.Separator(sav).grid(row=4, pady=2, padx=2, columnspan=3, sticky="ew")
            ent = Button(sav, text="Save", width=11)
            ent.bind("<Button-1>", savv)
            ent.grid(row=5, column=1, sticky="ew")
            sav.mainloop()

        win.destroy()
        root = Tk()

        root.iconbitmap('icon.ico')
        root.title("English and Hindi Voice Typing Editor")
        Label(root, text="English Speech to text:").grid(row=0, column=0, sticky=W)
        eng = Text(root, height=12, width=72, bd=5, font=("Times", 12))
        eng.grid(row=3, columnspan=3)
        se = Button(root, text="Speak English", width=11)
        se.bind("<Button-1>", speakeng)
        se.grid(row=6, column=0)
        es = Button(root, text="Clear English", width=11)
        es.bind("<Button-1>", cleareng)
        es.grid(row=6, column=1)
        ce = Button(root, text="Save English", width=11)
        ce.bind("<Button-1>", saveeng)
        ce.grid(row=6, column=2)
        Label(root, text="Hindi Speech to text:").grid(row=7, column=0, sticky=W)
        hin = Text(root, height=12, width=72, bd=5, font=("Times", 12))
        hin.grid(row=10, columnspan=3)
        sh = Button(root, text="Speak Hindi", width=11)
        sh.bind("<Button-1>", speakhin)
        sh.grid(row=13, column=0)
        hs = Button(root, text="Clear Hindi", width=11)
        hs.bind("<Button-1>", clearhin)
        hs.grid(row=13, column=1)
        ch = Button(root, text="Save Hindi", width=11)
        ch.bind("<Button-1>", savehin)
        ch.grid(row=13, column=2)
        ttk.Separator(root).grid(row=14, pady=2, padx=2, columnspan=3, sticky="ew")
        ex = Button(root, text="Exit", width=11)
        ex.bind("<Button-1>", exitf)
        ex.grid(row=16, columnspan=3, sticky="ew")
        root.mainloop()

    def exitwin(a):
        win.destroy()

    def test_folder(a):
        def cg(a):
            mfcc_arr = joblib.load('Training_mfcc_arr.pkl')
            y = joblib.load('Training_y.pkl')
            label = joblib.load('Training_label.pkl')

            def exitcg(a):
                cgroot.destroy()
            def preprocess_mfcc(mfcc):
                mfcc_cp = copy.deepcopy(mfcc)
                for i in range(mfcc.shape[1]):
                    mfcc_cp[:, i] = mfcc[:, i] - np.mean(mfcc[:, i])
                    mfcc_cp[:, i] = mfcc_cp[:, i] / np.max(np.abs(mfcc_cp[:, i]))
                return mfcc_cp

            def audio_popup():
                def play(a):
                    file = cg_dirname + "/" + current_test
                    PlaySound(file, SND_FILENAME | SND_ASYNC)

                def exi(a):
                    global flag_audio_pop
                    flag_audio_pop = 1
                    savp.destroy()

                savp = Tk()
                savp.iconbitmap('audio.ico')
                savp.wm_title("Audio Player")
                Label(savp,
                      text="Click on Play to play the following Audio file:\n" + current_test + "\nClick on Exit to close this window.").grid(
                    row=1, column=0, sticky="ew")
                se = Button(savp, text="Play", width=11)
                se.bind("<Button-1>", play)
                se.grid(row=2, column=0)
                es = Button(savp, text="Exit", width=11)
                es.bind("<Button-1>", exi)
                es.grid(row=2, column=1)
                savp.mainloop()

            def recognize_all(a):
                start = time.perf_counter()
                dirname = cg_dirname
                files = test_files
                Test_Result = []
                for j in range(len(files)):
                    start1 = time.perf_counter()
                    yTest, srTest = librosa.load(dirname + "/" + files[j])
                    mfccTest = librosa.feature.mfcc(yTest, srTest)
                    mfccTest = preprocess_mfcc(mfccTest)
                    dists = []
                    for i in range(len(mfcc_arr)):
                        mfcci = mfcc_arr[i]
                        disti = dtw(mfcci.T, mfccTest.T, dist=lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
                        dists.append(disti)
                    min_dist = min(dists)
                    min_dist_index = dists.index(min_dist)
                    pre = int(y[min_dist_index])
                    output = label[pre]
                    tt = time.perf_counter() - start1
                    output = "Input File : " + current_test + ".\nThe spoken word is : " + output + ".\nTime taken for Recognition : " + str(tt) + "\n"
                    micl.insert(INSERT, output)
                    Test_Result.append(label[pre])
                tt = time.perf_counter() - start
                output = "\nTotal Time taken for Recognizing "+str(len(test_files))+" Testing files : " +str(tt) + "\n"
                micl.insert(INSERT, output)
                #Accuracy
                eng_arr = ["aabe","baith","bera","eti","godh","hamar","hey","jaahun","kaabar" ,"kahat","karat","khaabe","koti","laika","mor","pirat" , "rengat" , "terat" , "toora" , "tuman"]
                j=0
                correct = 0
                total_files = len(test_files)
                for i in test_files:
                    lis = list(i.split('_'))
                    index = eng_arr.index(lis[0])
                    true_value = label[index]
                    if Test_Result[j]==true_value:
                        correct+=1
                    j+=1
                accuracy = (correct/total_files)*100
                output = "\nAccuracy of the complete Recognition : " + str(correct) + " out of " + str(total_files) + ".\nAccuracy percentage : "+str(accuracy)+"\n"
                micl.insert(INSERT, output)

            def selected_from_dd(*args):
                global current_test
                current_test = tkvar.get()
                t1 = threading.Thread(target=audio_popup)
                t1.start()

                start = time.perf_counter()
                yTest, srTest = librosa.load(cg_dirname + "/" + current_test)
                mfccTest = librosa.feature.mfcc(yTest, srTest)
                mfccTest = preprocess_mfcc(mfccTest)

                dists = []
                for i in range(len(mfcc_arr)):
                    mfcci = mfcc_arr[i]
                    disti = dtw(mfcci.T, mfccTest.T, dist=lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
                    dists.append(disti)
                # plt.plot(dists)
                min_dist = min(dists)
                min_dist_index = dists.index(min_dist)
                pre = int(y[min_dist_index])
                output = label[pre]
                tt = time.perf_counter()-start
                output = "Input File : "+str(current_test)+".\nThe spoken word is : "+str(output)+".\nTime taken for Recognition : "+str(tt)+"\n"
                sop.insert(INSERT, output)

                global flag_audio_pop
                if flag_audio_pop == 1:
                    t1.join()
                    flag_audio_pop = 0

            fol.destroy()
            cgroot = Tk()

            cgroot.iconbitmap('icon.ico')
            tkvar = StringVar(cgroot)

            cgroot.title("Chhattisgarhi Small Vocabulary Speech Recognition")
            drop_down_menu = OptionMenu(cgroot, tkvar, *test_files)
            Label(cgroot, text="Recognize a single file, Choose from below: ").grid(row=0, columnspan=2, sticky="w")
            drop_down_menu.grid(row=2, column=1, sticky="ew")
            tkvar.trace('w', selected_from_dd)
            sop = Text(cgroot, height=12, width=60, bd=5, font=("Times", 12))
            sop.grid(row=2, column=0)
            ttk.Separator(cgroot).grid(row=3, pady=2, padx=2, columnspan=3, sticky="ew")
            Label(cgroot, text="Recognize all the Audio files of Test folder: ").grid(row=4, columnspan=2, sticky="w")
            micl = Text(cgroot, height=12, width=60, bd=5, font=("Times", 12))
            micl.grid(row=5, column=0, sticky="w")
            reczall = Button(cgroot, text="Recognize All", width=11)
            reczall.bind("<Button-1>", recognize_all)
            reczall.grid(row=5, column=1, sticky="ew")
            ttk.Separator(cgroot).grid(row=6, pady=2, padx=2, columnspan=3, sticky="ew")
            ex = Button(cgroot, text="Exit", width=11)
            ex.bind("<Button-1>", exitcg)
            ex.grid(row=7, columnspan=3, sticky="ew")

            cgroot.mainloop()

        def askfolder(a):
            global cg_dirname
            cg_dirname = filedialog.askdirectory()
            folentry.insert(0, cg_dirname)
            global test_files
            test_files = [f for f in os.listdir(cg_dirname) if os.path.isfile(os.path.join(cg_dirname,f))]
            if "desktop.ini" in test_files:
                test_files.remove("desktop.ini")
            print(test_files)

        win.destroy()
        fol = Tk()

        fol.iconbitmap('save.ico')
        fol.title("Testing Folder Selection")
        Label(fol, text="Choose the folder containing Testing Audio files:").grid(row=0, column=0, sticky=W)
        folentry = Entry(fol, width=77)
        folentry.grid(row=1, sticky=W, column=0)
        ch = Button(fol, text="Browse")
        ch.bind("<Button-1>", askfolder)
        ch.grid(row=1, column=1, sticky=E)
        ch = Button(fol, text="Next")
        ch.bind("<Button-1>", cg)
        ch.grid(row=2, columnspan=2, sticky="ew")

        fol.mainloop()



    popup.destroy()
    win = Tk()

    win.iconbitmap('icon.ico')
    win.title("Select the language for Recognition")
    Label(win, text="English/Hindi Speech to text:").grid(row=0, column=0, sticky=W)
    se = Button(win, text="English/Hindi", width=11)
    se.bind("<Button-1>", enghin)
    se.grid(row=0, column=1, sticky="ew")
    ttk.Separator(win).grid(row=2, pady=2, padx=2, columnspan=3, sticky="ew")
    Label(win, text="Chhattisgarhi Small Vocabulary Recognition(Words listed below):").grid(row=4, column=0, sticky=W)
    words = Text(win, height=4, width=60, bd=5, font=("Times", 12))
    words.grid(row=6, column=0)
    words.insert(INSERT, "'आबे', 'बईठ', 'बेरा', 'एती', 'गोड़', 'हमर', 'हे', 'जाहूँ', 'काबर', 'कहत', 'करत', 'खाबे', 'कोति', 'लइका','मोर', 'पीरात', 'रेंगत', 'टेरत', 'टूरा', 'तुमन'")
    sh = Button(win, text="Chhattisgarhi", width=11)
    sh.bind("<Button-1>", test_folder)
    sh.grid(row=6, column=1, sticky="ew")
    ttk.Separator(win).grid(row=10, pady=2, padx=2, columnspan=3, sticky="ew")
    exx = Button(win, text="Exit", width=11)
    exx.bind("<Button-1>", exitwin)
    exx.grid(row=12, columnspan=3, sticky="ew")

    win.mainloop()





def genlist(a):
    mic_list = sr.Microphone.list_microphone_names()
    j = 1
    li = ""
    for i, microphone_name in enumerate(mic_list):
        temp = str(j)
        temp = temp + " - " + microphone_name + "\n"
        li = li + temp
        j += 1
    # print("\ngenlist's --\n",li)
    e = textbs["miclist"]
    # print("\ninslist's --\n", li)
    e.insert(INSERT, li)

popup = Tk()
popup.iconbitmap('mic.ico')
popup.wm_title("Microphone Confirmation")
Label(popup, text="Enter the serial number of the appropriate mic from the following list").grid(row=0,column=0,sticky=W)
micl = Text(popup, height=6, width=30, bd=9, font=("Times", 12))
micl.grid(row=1, columnspan=1, sticky = "ew")
textbs["miclist"] = micl
gl = Button(popup, text="Generate list", width=11)
gl.bind("<Button-1>",genlist)
gl.grid(row=1, column=1, sticky = "ew")
e = Entry(popup,width = 50)
e.grid(row=7,sticky = "ew")
entries["mic"] = e
ent = Button(popup, text="Submit", width=11)
ent.bind("<Button-1>", language_selection_window)
ent.grid(row=7, column=1, sticky = "ew")
popup.mainloop()