/// DataStructure.cs
/// 
/// Container for the struct definition and struct instances we
/// will use for each of the solver algorithms.
using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Text;

/// <summary>
/// Structure that will hold elements for each algorithm.
/// </summary>
public class DataStructure
{
    public struct bint {
        public ids left;
        public ids right;
        public bool isLeaf;

        public bint(ids l, ids r)
        {
            left = l;
            right = r
            isLeaf = l == null && r == null;
        }
    }
    public String PATH; 
    public struct ids {
        public List<String> labels;
        public List<Double[]> feats;
        public List<KeyValuePair<Double[], String>> comb;
        public ids(Object a) 
        {
            labels = new List<String>();
            feats = new List<Double[]>();
            comb = new List<KeyValuePair<Double[],String>>();
        }
    }
    public ids train_d;
    public ids val_d;
    StreamWriter writer;
    int callsToWrite = 0;
    int nCorrect = 0;
    int part;

    /// <summary>
    /// Write a line to the answer file.
    /// </summary>
    /// <param name="msg">String to write.</param>
    public void write(String msg)
    {
        if(!val_d.labels[callsToWrite++].Equals(msg) || (nCorrect++) == -1) { 
            Console.WriteLine(
                "--- Expected " + val_d.labels[callsToWrite-1] +
                " but got "+msg +" Accuracy: "+nCorrect/(double)callsToWrite);
        }
        writer.WriteLine(msg);
    }

    /// <summary>
    /// Return the number of training data points.
    /// </summary>
    /// <returns></returns>
    public int nTrain()
    {
        return train_d.feats.Count;
    }

    /// <summary>
    /// Initialize a new DataStructure. Mostly just need the path info
    /// here. Reads in the data files into the data structures.
    /// </summary>
    /// <param name="path">Example: "hw12data\digitsDataset"</param>
    /// <param name="ans">Example: "emailOutput1.csv"</param>
    /// <param name="dataFile">Example: trainFeatures.csv</param>
    /// <param name="labelFile">Example: trainLabels.csv</param>
    public DataStructure(   String path, String dataFile, String labelFile, 
                            String ans, int problem_part)
    {
        part = problem_part;
        train_d = new ids(null);
        val_d = new ids(null);
        PATH = path;
        Func <String[],Double[]> c2 = (x) => 
            { return (from y in x select Convert.ToDouble(y)).ToArray(); };
        String dataF = dataFile;
        String lblF = labelFile;
        String ansF = ans;
        writer = new StreamWriter(ans);
        using(StreamReader va_l = new StreamReader(PATH+"\\"+lblF))
        using(StreamReader va_f = new StreamReader(PATH+"\\"+dataF))
        using(StreamReader tr_l = new StreamReader(PATH+"\\trainLabels.csv"))
        using(StreamReader tr_f = new StreamReader(PATH+"\\trainFeatures.csv")) {
            String line;
            while((line = tr_f.ReadLine()) != null) {
                Double[] feature = c2(line.Split(','));
                String label = tr_l.ReadLine();
                
                train_d.feats.Add(feature);
                train_d.labels.Add(label);
                train_d.comb.Add(new KeyValuePair<double[],string>(feature, label));
            }
            while((line = va_f.ReadLine()) != null) { 
                Double[] feature = c2(line.Split(','));
                String label = va_l.ReadLine();

                val_d.feats.Add(feature);
                val_d.labels.Add(label);
                val_d.comb.Add(new KeyValuePair<double[],string>(feature, label));
            }
        }
    }
    
    ~DataStructure()
    {
        Console.WriteLine("Total accuracy: " + nCorrect/(double)val_d.feats.Count);
        try { 
            writer.Close();
        } catch(Exception e) { }
    }
}
