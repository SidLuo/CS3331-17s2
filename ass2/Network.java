/** Group z5096182 Guozhao Luo z5001159 Yang Mao
 *  COMP3331 Assignment2
 */

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class Network {
	static double[][] delays; // adjacency matrix
	static int[][] capacities;
	static double[][] ifPath;
	static int[][] numVCs;
	static int[] nodes;
	static ArrayList<Workload> workloads;

	public Network(String file) {
		delays = new double[26][26];
		capacities = new int[26][26];
		ifPath = new double[26][26];
		numVCs = new int[26][26];
		nodes = new int[26];
		workloads = new ArrayList<Workload>();

		for (int i = 0; i < 26; i++) {
			nodes[i] = 0;
			for (int j = 0; j < 26; j++) {
				capacities[i][j] = 0;
				numVCs[i][j] = 0;
				delays[i][j] = (double)Integer.MAX_VALUE;
				ifPath[i][j] = (double)Integer.MAX_VALUE;
			}
		}

		try {
			Scanner sc = new Scanner(new File(file));
			while (sc.hasNextLine()) {
				String nextLine = sc.nextLine();
				String details[] = nextLine.split(" ");

				int source = convert2Int(details[0]);
				int target = convert2Int(details[1]);
				double delay = Double.parseDouble(details[2]);
				int capacity = Integer.parseInt(details[3]);

				addEdge(source, target, delay, capacity);
				addEdge(target, source, delay, capacity);
			}
			sc.close();
		} catch (IOException e) {
		}

	}

	public static int convert2Int(String a) {
		return Character.getNumericValue(a.charAt(0)) - 9;
	}

	public static String convert2Str(int a) {
		return Character.toString((char) (a + 64));
	}

	public void addEdge(int source, int target, double delay, int capacity) {
		boolean flag = true;
		int i = 0;
		for (i = 0; i < nodes.length; i++) {
			if (source == nodes[i]) {
				flag = false;
			}
			if (nodes[i] == 0)
				break;
		}
		if (flag) {
			nodes[i] = source;
		}
		delays[source][target] = delay;
		capacities[source][target] = capacity;
		ifPath[source][target] = 1;

	}

	public static void addrequests(String file, Network net) {
		try {
			Scanner sc = new Scanner(new File(file));
			while (sc.hasNextLine()) {
				String nextLine = sc.nextLine();
				String details[] = nextLine.split(" ");

				int source = convert2Int(details[1]);
				int target = convert2Int(details[2]);
				double startT = Double.parseDouble(details[0]);
				double duration = Double.parseDouble(details[3]);

				Workload c = new Workload(source, target, startT, duration);
				workloads.add(c);
			}
			sc.close();
		} catch (IOException e) {
		}
	}

}
