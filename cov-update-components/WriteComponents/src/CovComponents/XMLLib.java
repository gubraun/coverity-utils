package CovComponents;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class XMLLib {

	private List<ComponentMap> compmap; 
	Document dom;

	public XMLLib(List<ComponentMap> compmap) {

		// Init List
		this.compmap = compmap;
	}
	
	public void runParseFile() {
		
		//parse the xml file and get the dom object
		parseXmlFile();
		
		//get each employee element and create a Employee object
		parseDocument();		
	}
	
	private void parseXmlFile(){
		//get the factory
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		
		try {
			
			//Using factory get an instance of document builder
			DocumentBuilder db = dbf.newDocumentBuilder();
			
			//parse using builder to get DOM representation of the XML file
			dom = db.parse("cmaps.xml");
			
		}catch(ParserConfigurationException pce) {
			pce.printStackTrace();
		}catch(SAXException se) {
			se.printStackTrace();
		}catch(IOException ioe) {
			ioe.printStackTrace();
		}	
	}
	
	private void parseDocument(){
		//get the root elememt
		Element docEle = dom.getDocumentElement();
		
		//get a nodelist of <ComponentMap> elements
		NodeList nl = docEle.getElementsByTagName("ComponentMap");
		
		//System.out.println("N1: " + nl + "Length: " + nl.getLength());
		
		if(nl != null && nl.getLength() > 0) {
			for(int i = 0 ; i < nl.getLength();i++) {
				
				//get the component map element
				Element cm = (Element)nl.item(i);
				
				//get the componentmap object
				ComponentMap CM = parseMapElement(cm);
				
				//add it to list
				compmap.add(CM);
			}
		}
	}
	
	private ComponentMap parseMapElement(Element ME){

		String name = ME.getAttribute("Name");
		System.out.println("MAP ==> " + name);
		String description = getTextValue(ME, "Description");
		System.out.println("Description ==> " + description);
		
		List<Component> ComponentList = new ArrayList<Component>();
		List<PathRule> PathRuleList = new ArrayList<PathRule>();
		List<DefectRule> DefectRuleList = new ArrayList<DefectRule>();

		NodeList nl = ME.getElementsByTagName("Component");
		if(nl != null && nl.getLength() > 0) {
			for(int i = 0 ; i < nl.getLength();i++) {
				
				//get the component element
				Element c = (Element)nl.item(i);
				
				//get the componentmap object
				Component C = parseComponentElement(c);
				
				//add it to list
				ComponentList.add(C);
			}
		}
		
		nl = ME.getElementsByTagName("PathRule");
		if(nl != null && nl.getLength() > 0) {
			for(int i = 0 ; i < nl.getLength();i++) {
				Element pr = (Element)nl.item(i);
				PathRule PR = parsePathRuleElement(pr);
				PathRuleList.add(PR);
			}
		}
		
		nl = ME.getElementsByTagName("DefectRule");
		if(nl != null && nl.getLength() > 0) {
			for(int i = 0 ; i < nl.getLength();i++) {
				Element dr = (Element)nl.item(i);
				DefectRule DR = parseDefectRuleElement(dr);
				DefectRuleList.add(DR);
			}
		}

		ComponentMap CM = new ComponentMap(name, description, ComponentList, PathRuleList, DefectRuleList);
		
		return CM;
	}

	private Component parseComponentElement(Element CE){

		String name = CE.getAttribute("Name");
		//String exclude = getTextValue(CE, "Exclude");
		List<RoleAssignment> RoleAssignList = new ArrayList<RoleAssignment>();
		List<String> SubscriberList = new ArrayList<String>();
		
		NodeList nl = CE.getElementsByTagName("RoleAssignmentGroup");
		if(nl != null && nl.getLength() > 0) {
			for(int i = 0 ; i < nl.getLength();i++) {
				
				//get the groupperm element
				Element ra = (Element)nl.item(i);
				
				//get the group perm object
				RoleAssignment RA = parseRoleAssignElement(ra);
				
				//add it to list
				RoleAssignList.add(RA);
			}
		}
		
		nl = CE.getElementsByTagName("Subscriber");
		if(nl != null && nl.getLength() > 0) {
			for(int i = 0 ; i < nl.getLength();i++) {
				
				//get the groupperm element
				Element s = (Element)nl.item(i);
				
				//get the subscriber name
				String S = parseSubscriberElement(s);
				
				//add it to list
				SubscriberList.add(S);
			}
		}
		
		Component C = new Component(name, RoleAssignList, SubscriberList);
		
		return C;
	}
	
	private PathRule parsePathRuleElement(Element PRE){

		String name = PRE.getAttribute("Name");
		String pathpattern = getTextValue(PRE, "Pattern");
		PathRule PR = new PathRule(name, pathpattern);
		return PR;
	}
	
	private DefectRule parseDefectRuleElement(Element DRE){

		String name = DRE.getAttribute("Name");
		String owner = getTextValue(DRE, "Owner");
		DefectRule DR = new DefectRule(name, owner);
		return DR;
	}
	
	private RoleAssignment parseRoleAssignElement(Element RAE){

		String gid = RAE.getAttribute("Name");
		String domain = getTextValue(RAE, "Domain");
		String rtype = getTextValue(RAE, "Type");
		String name = getTextValue(RAE, "Name");
		String level = getTextValue(RAE, "Level");
		String username = getTextValue(RAE, "Username");			
		RoleAssignment RA = new RoleAssignment(gid,domain,rtype,name,level,username);
		return RA;
	}
	
	private String parseSubscriberElement(Element SE){

		String name = SE.getAttribute("Name");
		return name;
	}

	/**
	 * I take a xml element and the tag name, look for the tag and get
	 * the text content 
	 * i.e for <employee><name>John</name></employee> xml snippet if
	 * the Element points to employee node and tagName is name I will return John  
	 * @param ele
	 * @param tagName
	 * @return
	 */
	private String getTextValue(Element ele, String tagName) {
		String textVal = null;
		NodeList nl = ele.getElementsByTagName(tagName);
		if(nl != null && nl.getLength() > 0) {
			Element el = (Element)nl.item(0);
			textVal = el.getFirstChild().getNodeValue();
		}

		return textVal;
	}

	
	/**
	 * Calls getTextValue and returns a int value
	 * @param ele
	 * @param tagName
	 * @return
	 */
	private int getIntValue(Element ele, String tagName) {
		//in production application you would catch the exception
		return Integer.parseInt(getTextValue(ele,tagName));
	}
	
}

