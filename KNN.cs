/// KNN.cs
/// 
/// @brief      Implementation of K-Nearest Neighbor classifier. Part of a 
///             homework set for CS170 at UC Berkeley.
/// @author     John Wilkey
using System;
using System.Collections.Generic;
using System.Collections;
using System.IO;
using System.Linq;

public class KNN
{
    /// <summary>
    /// Main program entry point.
    /// </summary>
    public void run(int k, DataStructure ds) {        
        for(var i = 0;i < ds.val_d.feats.Count;i++) {    
            Dictionary<int, double> matches = new Dictionary<int,double>();
            for(var j = 0; j < ds.train_d.feats.Count; j++) {
                Double totalErr = 0;
                Double[] t_feat = ds.train_d.feats[j];
                for(var kk = 0;kk < t_feat.Length;kk++)
                    totalErr += Math.Pow((t_feat[kk] - ds.val_d.feats[i][kk]), 2);
                matches.Add(j, Math.Sqrt(totalErr));
            }
            List<KeyValuePair<int, double>> l = matches.ToList();
            l.Sort((x,y) => { return x.Value.CompareTo(y.Value); });
            l = l.Take(k).ToList();
            Dictionary<String, Int32> winners = new Dictionary<String,int>();
            foreach(var neighbor in l) {
                String key = ds.train_d.labels[neighbor.Key];
                if(winners.ContainsKey(key)) {
                    winners[key] += 1;
                } else {
                    winners[key] = 1;
                }
            }
            List<KeyValuePair<String, Int32>> cand = winners.ToList();
            cand.Sort((x,y) => { return -x.Value.CompareTo(y.Value);});
            List<KeyValuePair<String, Int32>> maxCntWinners = 
                (from x in cand where x.Value == cand[0].Value select x)
                .ToList();
            List<KeyValuePair<Int32,Double>> res = 
                (from x in l 
                where ds.train_d.labels[x.Key] == maxCntWinners[0].Key 
                select x).ToList();
            res.Sort((x,y) => { return x.Value.CompareTo(y.Value); });
            var finAns = ds.train_d.labels[res.Take(1).ToList()[0].Key];
            ds.write(finAns);
        }
    }
}
