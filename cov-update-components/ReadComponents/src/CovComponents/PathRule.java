package CovComponents;

public class  PathRule {

	private String name; // name of component
	private String pathpattern;
		
	public PathRule(String name){
		this.name = name;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getPathPattern() {
		return pathpattern;
	}
	public void setPathPattern(String pathpattern) {
		this.pathpattern = pathpattern;
	}

}