/** Group z5096182 Guozhao Luo z5001159 Yang Mao
 *  COMP3331 Assignment2
 */

public class Workload{
	public int source;
	public int target;
	public double startT;
	public double duration;
	public boolean Success = false;
	public boolean Blocked = false;
	
	public Workload(int s, int t, double sT, double d){
		source = s;
		target = t;
		startT = sT;
		duration = d;
		
	}

	public Object getActualPathTaken() {
		return null;
	}
}
