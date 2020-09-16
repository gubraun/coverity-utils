package CovComponents;

public class  RoleAssignment {

	private String gid; // Group ID
	private String rtype; // Role Assignment Type
	private String name; // Role Name
	private String type;  // type --> stream, project, global
	private String username; // User Name to Whom the Role Applies
	private String domain; // LDAP Domain
			
	public RoleAssignment(String gid){
		this.gid = gid;
	}
	public RoleAssignment(String gid, String rtype, String name, String type, String username){
		this.gid = gid;
		this.rtype = rtype;
		this.name = name;
		this.type = type;
		this.username = username;
	}
	public RoleAssignment(String gid, String domain, String rtype, String name, String type, String username){
		this.gid = gid;
		this.domain = domain;
		this.rtype = rtype;
		this.name = name;
		this.type = type;
		this.username = username;
	}
	public String getName() {
		return name;
	}
	public void setName(String name){
		this.name = name;
	}
	public void setType(String type) {
		this.type = type;
	}
	public String getType() {
		return type;
	}
	public void setGid(String gid) {
		this.gid = gid;
	}
	public String getGid() {
		return gid;
	}
	public void setRtype(String rtype) {
		this.rtype = rtype;
	}
	public String getRtype() {
		return rtype;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	public String getUsername() {
		return username;
	}
	public void setDomain(String domain) {
		this.domain = domain;
	}
	public String getDomain() {
		return domain;
	}
	
}
