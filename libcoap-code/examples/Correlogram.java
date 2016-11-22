package com.parking.stability;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;


public class Correlogram {

	private static BufferedReader delete,put,get;

	public static void main(String[] args) throws IOException {
//		delete = new BufferedReader(new FileReader("/home/paridhika/git/CoAP_Parking/libcoap-code/examples/Results/run1/80/delete_simulation_service_time_80_run1.csv"));
//		put = new BufferedReader(new FileReader("/home/paridhika/git/CoAP_Parking/libcoap-code/examples/Results/run1/80/put_simulation_service_time_80_run1.csv"));
//		get = new BufferedReader(new FileReader("/home/paridhika/git/CoAP_Parking/libcoap-code/examples/Results/run1/80/get_simulation_service_time_80_run1.csv"));

		delete = new BufferedReader(new FileReader("Results/run1/80/delete_simulation_service_time_80_run1.csv"));
		put = new BufferedReader(new FileReader("Results/run1/80/put_simulation_service_time_80_run1.csv"));
		get = new BufferedReader(new FileReader("Results/run1/80/get_simulation_service_time_80_run1.csv"));

		ArrayList<Double> r1 = new ArrayList<Double>();
		ArrayList<Double> r2 = new ArrayList<Double>();
		ArrayList<Double> r3 = new ArrayList<Double>();
		
		ArrayList<Double> w1 = new ArrayList<Double>();
		ArrayList<Double> w2 = new ArrayList<Double>();
		ArrayList<Double> w3 = new ArrayList<Double>();
		double[] mean = {0.0d,0.0d,0.0d};
		double[] SD = {0.0d,0.0d,0.0d};
		double[] confidence = {0.0d,0.0d,0.0d};
		String data_delete,data_put,data_get;
		delete.readLine();
		get.readLine();
		put.readLine();
		while ((data_delete = delete.readLine()) != null) {
			double value = Double.valueOf(data_delete.split(",")[2]);
			w1.add(value);
			mean[0] += value;
		}
		while ((data_put = put.readLine()) != null) {
			double value = Double.valueOf(data_put.split(",")[2]);
			w2.add(value);
			mean[1] += value;
		}
		while ((data_get = get.readLine()) != null) {
			double value = Double.valueOf(data_get.split(",")[2]);
			w3.add(value);
			mean[2] += value;
		}
		mean[0] /= w1.size();
		mean[1] /= w2.size();
		mean[2] /= w3.size();
		for (int j = 0; j < w1.size(); j++){
			double l = w1.get(j) - mean[0];
			SD[0] += l * l;
		}
		for (int j = 0; j < w2.size(); j++){
			double l = w2.get(j) - mean[1];
			SD[1] += l * l;
		}
		for (int j = 0; j < w3.size(); j++){
			double l = w3.get(j) - mean[2];
			SD[2] += l * l;
		}
		for (int k = 1; k < (w1.size()/4); k++){
			double numerator = 0d;
			for (int i = 0; i < (w1.size() - k); i++) {
				double l = w1.get(i) - mean[0];
				double m = w1.get(i + k) - mean[0];
				numerator += l * m;
			}
			r1.add(numerator / SD[0]);
		}
		for (int k = 1; k < (w2.size()/4); k++){
			double numerator = 0d;
			for (int i = 0; i < (w2.size() - k); i++) {
				double l = w2.get(i) - mean[1];
				double m = w2.get(i + k) - mean[1];
				numerator += l * m;
			}
			r2.add(numerator / SD[1]);
		}
		for (int k = 1; k < (w3.size()/4); k++){
			double numerator = 0d;
			for (int i = 0; i < (w3.size() - k); i++) {
				double l = w3.get(i) - mean[2];
				double m = w3.get(i + k) - mean[2];
				numerator += l * m;
			}
			r3.add(numerator / SD[2]);
		}
		
		SD[0] = Math.sqrt(SD[0] / w1.size());
		SD[1] = Math.sqrt(SD[1] / w2.size());
		SD[2] = Math.sqrt(SD[2] / w3.size());
		confidence[0] = 1.96 * SD[0] / Math.sqrt(w1.size());
		confidence[1] = 1.96 * SD[1] / Math.sqrt(w2.size());
		confidence[2] = 1.96 * SD[2] / Math.sqrt(w3.size());
		System.out.println("Delete: " + mean[0] + " Standard Diviation: " + SD[0] + " confidence: "	+ confidence[0] );
		System.out.println("Put: " + mean[1] + " Standard Diviation: " + SD[1] + " confidence: "	+ confidence[1] );
		System.out.println("Get: " + mean[2] + " Standard Diviation: " + SD[2] + " confidence: "	+ confidence[2] );
		
		FileWriter correlation = new FileWriter("Correlogram.csv");
		correlation.append("Delete_Lag");
		correlation.append(",");
		correlation.append("Correlation");
		for(int i = 0; i < r1.size(); i++){
			correlation.append("\n");
			correlation.append(String.valueOf(i));
			correlation.append(",");
			correlation.append(Double.toString(r1.get(i)));
		}
		correlation.append("\n");
		correlation.append("Put_Lag");
		correlation.append(",");
		correlation.append("Correlation");
		for(int i = 0; i < r2.size(); i++){
			correlation.append("\n");
			correlation.append(String.valueOf(i));
			correlation.append(",");
			correlation.append(Double.toString(r2.get(i)));
		}
		correlation.append("\n");
		correlation.append("Get_Lag");
		correlation.append(",");
		correlation.append("Correlation");
		for(int i = 0; i < r3.size(); i++){
			correlation.append("\n");
			correlation.append(String.valueOf(i));
			correlation.append(",");
			correlation.append(Double.toString(r3.get(i)));
		}
		
		correlation.flush();
		correlation.close();
	}
}
