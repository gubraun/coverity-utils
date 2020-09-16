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

public class ComponentMap {

	private String cmapname;
	private String description;
	private List<Component> components;
	private List<PathRule> pathrules;
	private List<DefectRule> defectrules;
	
	public ComponentMap(String cmapname) {
		this.cmapname = cmapname;
		this.components = new ArrayList<Component>();
		this.pathrules = new ArrayList<PathRule>();
		this.defectrules = new ArrayList<DefectRule>();
	}
	public ComponentMap(String cmapname, String description) {
		this.cmapname = cmapname;
		this.description = description;
		this.components = new ArrayList<Component>();
		this.pathrules = new ArrayList<PathRule>();
		this.defectrules = new ArrayList<DefectRule>();
	}
	public ComponentMap(String cmapname, String description, List<Component> components, List<PathRule> pathrules, List<DefectRule> defectrules) {
		this.cmapname = cmapname;
		this.description = description;
		this.components = components;
		this.pathrules = pathrules;
		this.defectrules = defectrules;
	}
	public String getCmapname() {
		return cmapname;
	}
	public void setCmapname(String cmapname) {
		this.cmapname = cmapname;
	}
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public List<Component> getComponents() {
		return components;
	}
	public void setComponent(Component component) {
		this.components.add(component);
	}
	public List<PathRule> getPathRules() {
		return pathrules;
	}
	public void setPathRule(PathRule pathrule) {
		this.pathrules.add(pathrule);
	}
	public List<DefectRule> getDefectRules() {
		return defectrules;
	}
	public void setDefectRule(DefectRule defectrule) {
		this.defectrules.add(defectrule);
	}
}
