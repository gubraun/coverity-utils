package CovComponents;

import javax.xml.ws.WebServiceRef;
import java.net.URL;
import javax.xml.namespace.QName;
import javax.xml.ws.BindingProvider;
import javax.xml.ws.WebServiceException;
import javax.xml.ws.soap.SOAPFaultException;
import javax.xml.ws.handler.Handler;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

public class  Component {

	private String name;	// Write this map name scoped ... e.g., test1.comp1
	private boolean excludecomp;
	private List<RoleAssignment> roleassign;
	private List<String> subscribers;
		
	public Component(String name){
		this.name = name;
		this.roleassign = new ArrayList<RoleAssignment>();
		this.subscribers = new ArrayList<String>();
	}
	public Component(String name, List<RoleAssignment> roleassign) {
		this.name = name;
		this.roleassign = roleassign;
	}
	public Component(String name, List<RoleAssignment> roleassign, List<String> subscribers) {
		this.name = name;
		this.roleassign = roleassign;
		this.subscribers = subscribers;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setExcludeComponent(boolean excludecomp){
		this.excludecomp = excludecomp;
	}
	public boolean getExcludeComponent(){
		return excludecomp;
	}
	public void setSubscriber(String S){
		this.subscribers.add(S);
	}
	public void setRoleAssignm(RoleAssignment roleassign){
		this.roleassign.add(roleassign);
	}
	public List<RoleAssignment> getRoleAssign() {
		return roleassign;
	}
	public List<String> getSubscribers() {
		return subscribers;
	}
}
