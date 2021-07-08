/** Group z5096182 Guozhao Luo z5001159 Yang Mao
 *  COMP3331 Assignment2
 */


import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;

public class RoutingPerformance {
	
	/*
	 * NETWORK SCHEME- type of argument that is evaluated ROUTING SCHEME-
	 * SHP,SDP,LLP TOPOLOGY FILE WORKLOAD FILE-virtual network connection
	 * requests PACKET_RATE- positive integer that shows the number of packets
	 * per second
	 * 
	 */

	/*
	 * NEED the following statistics
	 * 
	 * total number of virtual connection requests total number of packets
	 * number of successfully routed packets percentage of successfully routed
	 * packets number of blocked packets percentage of blocked packets average
	 * number of hops per circuit average cumulative propagation delay per
	 * circuit
	 * 
	 */

	static int numberOfWorkloads = 0;
	static int numberOfSuccessWorkload = 0;
	static int numberOfBlockedWorkload = 0;
	static int numberOfPackets = 0;
	static int numberOfSuccessPackets = 0;
	static int numberOfBlockedPackets = 0;

	static double Hops = 0.0;
	static double cumDelay = 0.0;
	static long startTime;
	static String routingScheme;
	static double packetSpeed;

	@SuppressWarnings("rawtypes")
	public static void main(String args[]) {
		double currentTime = 0;
        // Arguments
        String scheme = args[0]; // CIRCUIT PACKET
		routingScheme = args[1]; // SDP LLP
		String topologyFile = args[2];
		String workloadFile = args[3];
		int packetRate = Integer.parseInt(args[4]);
		packetSpeed = 1 / (double) packetRate;

		Network myNetwork = new Network(topologyFile);
		Network.addrequests(workloadFile, myNetwork);
		
		numberOfWorkloads = Network.workloads.size();

		double maxTimeRun = 0.0;
		for (Workload c : Network.workloads) {
			if ((c.duration + c.startT > maxTimeRun))
				maxTimeRun = c.duration + c.startT;
		}

		ArrayList<Integer> path = new ArrayList<Integer>();
		HashMap<Double, ArrayList<Integer>> ram = new HashMap<Double, ArrayList<Integer>>();

		for (Workload current : Network.workloads) {
			double Delay = 0;
			boolean success = true;
			int packets = (int) (current.duration / packetSpeed);
			currentTime = current.startT;
			path = DijkstraAlgorithm(current);

			Iterator<Entry<Double, ArrayList<Integer>>> it = ram.entrySet().iterator();
			while (it.hasNext()) {
				HashMap.Entry pair = (HashMap.Entry) it.next();
				if ((double) (pair.getKey()) < currentTime) {
					@SuppressWarnings("unchecked")
					ArrayList<Integer> tem = (ArrayList<Integer>) pair.getValue();
					for (int i = 0; i < tem.size() - 1; i++) {
						Network.numVCs[tem.get(i)][tem.get(i + 1)]--;
						Network.numVCs[tem.get(i + 1)][tem.get(i)]--;
					}
				}
			}

			for (int i = 0; i < path.size() - 1; i++) {
				Delay = Delay + Network.delays[path.get(i)][path.get(i + 1)];
				if ((Network.numVCs[path.get(i)][path.get(i + 1)]
						+ 1) > (Network.capacities[path.get(i)][path.get(i + 1)] + 1)) {
					success = false;
					break;
				}
			}

			numberOfPackets += packets;
			if (success) {
				for (int i = 0; i < path.size() - 1; i++) {
					Network.numVCs[path.get(i)][path.get(i + 1)]++;
					Network.numVCs[path.get(i + 1)][path.get(i)]++;
				}

				double key = Delay + current.startT + current.duration;
				ram.put(key, path);

				numberOfSuccessWorkload++;
				Hops += path.size() - 1;
				cumDelay += Delay;
				numberOfSuccessPackets = numberOfSuccessPackets + packets;

			} else {
				numberOfBlockedWorkload++;
				numberOfBlockedPackets = numberOfBlockedPackets + packets;
			}
		}
		print();
	}

	private static ArrayList<Integer> DijkstraAlgorithm(Workload current) {
		ArrayList<Integer> path = new ArrayList<Integer>();
		double[][] Weight = new double[26][26];

		if (routingScheme.equals("SHP")) {
			Weight = Network.ifPath;
		} else if (routingScheme.equals("SDP")) {
			Weight = Network.delays;
		} else if (routingScheme.equals("LLP")) {
			for (int i = 0; i < 26; i++) {
				for (int j = 0; j < 26; j++) {
					if(Network.capacities[i][j]==0){
						Weight[i][j] = Integer.MAX_VALUE;
						Weight[j][i] = Integer.MAX_VALUE;
					}else{
						Weight[i][j] = Weight[j][i] = 10000*(double) Network.numVCs[i][j] / (double) Network.capacities[i][j];
					}
				}
			}
		}
		path = dijkstra(Weight, current.source, current.target);
		return path;
	}
	
	static ArrayList<Integer> dijkstra(double graph[][], int src, int V) {
		ArrayList<Integer> path = new ArrayList<Integer>();
		int[] P = new int[Network.nodes.length];
		for (int i = 0; i < Network.nodes.length; i++) {
			P[i] = Integer.MAX_VALUE;
		}
		double dist[] = new double[Network.nodes.length];
		Boolean sptSet[] = new Boolean[Network.nodes.length];
		for (int i = 0; i < Network.nodes.length; i++) {
			dist[i] = Integer.MAX_VALUE;
			sptSet[i] = false;
		}
		dist[src] = 0;

		for (int count = 0; count < Network.nodes.length - 1; count++) {
			double min = Integer.MAX_VALUE;
			int u = -1;

			for (int v = 0; v < Network.nodes.length; v++) {
				if (sptSet[v] == false && dist[v] <= min) {
					min = dist[v];
					u = v;
				}
			}
			sptSet[u] = true;
			for (int v = 0; v < Network.nodes.length - 1; v++)
				if (!sptSet[v] && graph[u][v] != Integer.MAX_VALUE && dist[u] != Integer.MAX_VALUE
						&& dist[u] + graph[u][v] < dist[v]) {
					dist[v] = dist[u] + graph[u][v];
					P[v] = u;
				}
		}
		path.add(V);
		int loc = V;
		while (P[loc] != src) {
			path.add(0, P[loc]);
			loc = P[loc];
		}
		path.add(0, src);
		return path;
	}

	private static void print() {
		System.out.println("total number of virtual connection requests: " + numberOfWorkloads);
		System.out.println("total number of packets: " + numberOfPackets);
		System.out.println("number of successfully routed packets: " + numberOfSuccessPackets);
		Double percentageofsuccessfullyroutedpackets = BigDecimal
				.valueOf(100 * (double) numberOfSuccessPackets / (double) numberOfPackets)
				.setScale(2, RoundingMode.HALF_UP).doubleValue();
		System.out.println("percentage of successfully routed packets: " + percentageofsuccessfullyroutedpackets);

		System.out.println("number of blocked packets: " + numberOfBlockedPackets);
		Double percentageofblockedpackets = BigDecimal
				.valueOf(100 * (double) numberOfBlockedPackets / (double) numberOfPackets)
				.setScale(2, RoundingMode.HALF_UP).doubleValue();
		System.out.println("percentage of blocked packets: " + percentageofblockedpackets);

		double averageNumHops = Hops / numberOfSuccessWorkload;
		Double castedHops = BigDecimal.valueOf(averageNumHops).setScale(2, RoundingMode.HALF_UP).doubleValue();
		System.out.println("average number of hops per circuit: " + castedHops);
		Double percentDelay = BigDecimal.valueOf(cumDelay / numberOfSuccessWorkload).setScale(2, RoundingMode.HALF_UP)
				.doubleValue();
		System.out.println("average cumulative propagation delay per circuit: " + percentDelay);
	}

}
