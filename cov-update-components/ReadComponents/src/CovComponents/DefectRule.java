package CovComponents;

public class  DefectRule {

	private String name; // name of the component
	private String owner; // who own's the component
		
	public DefectRule(String name){
		this.name = name;
	}
	public String getName() {
		return name;
	}
    public void setName(String name){
		this.name = name;
	}
    public String getOwner() {
		return owner;
	}
    public void setOwner(String owner){
		this.owner = owner;
	}
}