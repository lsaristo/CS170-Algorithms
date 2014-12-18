/// Driver.cs
/// 
/// Simple driver program to run both algorithms. The algorithms
/// themselves deal with read and writing to files so all we need
/// to do here is call them with the appropriate filenames.
using System;

/// <summary>
/// Primary driver for the two algorithms. Execution starts in here.
/// </summary>
class Driver
{
    /// <summary>
    /// Main program entry point.
    /// </summary>
    /// <param name="args"></param>
    public static void Main(String[] args)
    {
        if(args.Length != 3) {
            Console.WriteLine("Usage: [program].exe k feature_file label_file");
            return;
        }
        int k = Convert.ToInt32(args[0]);
        
        DataStructure ds1 = new DataStructure(   @"hw12data\digitsDataset", args[1],
                                                args[2],"digitsOutput"+k+".csv",1);
        KNN knn = new KNN();
        knn.run(k, ds1);
    }
}
