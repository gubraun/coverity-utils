package CovComponents;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Text;

//For jdk1.5 with built in xerces parser
import com.sun.org.apache.xml.internal.serialize.OutputFormat;
import com.sun.org.apache.xml.internal.serialize.XMLSerializer;

//@SuppressWarnings("all")
public class XMLLib {

	private List<ComponentMap> compmap; 
	Document dom;

	public XMLLib(List<ComponentMap> compmap) {

		// Init List
		this.compmap = compmap;
		
		//Get a DOM object
		createDocument();
	}

	public void runCreateFile(){
		System.out.println(" ");
		System.out.println("------------------------------------");
		System.out.println("WRITING COMPONENTS TO FILE CMAPS.XML");
		System.out.println("------------------------------------");
		createDOMTree();
		printToFile();
		System.out.println(" ");
		System.out.println("SUCCESSFUL FILE GENERATION ==> cmaps.xml");
		System.out.println(" ");
	}

	/**
	 * Using JAXP in implementation independent manner create a document object
	 * using which we create a xml tree in memory
	 */
	private void createDocument() {

		//get an instance of factory
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		try {
		//get an instance of builder
		DocumentBuilder db = dbf.newDocumentBuilder();

		//create an instance of DOM
		dom = db.newDocument();

		}catch(ParserConfigurationException pce) {
			//dump it
			System.out.println("Error while trying to instantiate DocumentBuilder " + pce);
		}
		
		//System.exit(1);

	}

	/**
	 * The real workhorse which creates the XML structure
	 */
	private void createDOMTree(){

		//create the root element <CMAP>
		Element rootEle = dom.createElement("CMaps");
		dom.appendChild(rootEle);

		 for(int i=0; i < compmap.size(); i++)
         {
			ComponentMap CM = compmap.get(i);
         	System.out.println("====> " + CM.getCmapname());       	
         	Element ME = createMapElement(CM);
         	rootEle.appendChild(ME);
         }
		 
		// System.exit(1);
	}

	private Element createMapElement(ComponentMap CM){

		Element ME = dom.createElement("ComponentMap");
		ME.setAttribute("Name", CM.getCmapname());
		String Description = CM.getDescription();
		String Empty = "";
		
		if(Description == null)
		{
			//Element DSE = dom.createElement("Description");
			//Text DST = dom.createTextNode("null");
			//DSE.appendChild(DST);
			//ME.appendChild(DSE);
		}
		else if(Description.equals(Empty))
		{		
		}
		else
		{
			Element DSE = dom.createElement("Description");
			Text DST = dom.createTextNode(CM.getDescription());
			DSE.appendChild(DST);
			ME.appendChild(DSE);
		}
		
		for(int i=0; i < CM.getComponents().size(); i++)
        {
			Component C = CM.getComponents().get(i);
			String s = C.getName();
        	String t = "Other";
          	if(s.equals(t)) continue;
        	//System.out.println("SizeC: " + CM.getComponents().size() + "========> " + C.getName());       	
        	Element CE = createComponentElement(C);
        	ME.appendChild(CE);
        }
		for(int i=0; i < CM.getPathRules().size(); i++)
        {
			PathRule PR = CM.getPathRules().get(i);
        	//System.out.println("SizePR: " + CM.getPathRules().size() + "========> " + PR.getName());       	
        	Element PE = createPathRuleElement(PR);
        	ME.appendChild(PE);
        }
		for(int i=0; i < CM.getDefectRules().size(); i++)
        {
			DefectRule DR = CM.getDefectRules().get(i);
			if(DR.getOwner() == null) continue;
			System.out.println("SizeDR: " + CM.getDefectRules().size() + "========> " + DR.getName());       	
        	Element DE = createDefectRuleElement(DR);
        	ME.appendChild(DE);
        }

		return ME;
	}
	
	private Element createComponentElement(Component C){
		Element CE = dom.createElement("Component");
		CE.setAttribute("Name", C.getName());
		
		//System.out.println("SizeRA: " + C.getRoleAssign().size() );
		
		for(int i=0; i < C.getRoleAssign().size(); i++)
        {
			RoleAssignment RA = C.getRoleAssign().get(i);
			//System.out.println("SizeRA: " + C.getRoleAssign().size() + "========> " + RA.getGid());       	
        	Element RE = createRoleAssignmentElement(RA);
        	CE.appendChild(RE);
        }
        		
		for(int i=0; i < C.getSubscribers().size(); i++)
        {
			String S = C.getSubscribers().get(i);
			//System.out.println("SizeSUB: " + C.getSubscribers().size() + "========> " + S);       	
        	Element SE = createSubscriberElement(S);
        	CE.appendChild(SE);
        }
		
		return CE;
	}
	
	private Element createRoleAssignmentElement(RoleAssignment RA){
		Element RAE = dom.createElement("RoleAssignmentGroup");
		RAE.setAttribute("Name", RA.getGid());
		/*
		System.out.println("GID: " + RA.getGid() );
		System.out.println("RType: " + RA.getRtype() );
		System.out.println("Type: " + RA.getType() );
		System.out.println("Name: " + RA.getName() );
	    System.out.println("UN: " + RA.getUsername() );
		*/
		if(!(RA.getDomain() == null))
		{
			Element RAD = dom.createElement("Domain");
			System.out.println("Domain: " + RA.getDomain());
			Text RD = dom.createTextNode(RA.getDomain());
			RAD.appendChild(RD);
			RAE.appendChild(RAD);
		}
		if(!(RA.getRtype() == null))
		{
			Element RAT = dom.createElement("Type");
			System.out.println("Type: " + RA.getRtype() );
			Text RT = dom.createTextNode(RA.getRtype());
			RAT.appendChild(RT);
			RAE.appendChild(RAT);
		}
		if(!(RA.getName() == null))
		{
			Element RAN = dom.createElement("Name");
			System.out.println("Name: " + RA.getName() );
			Text RT2 = dom.createTextNode(RA.getName());
			RAN.appendChild(RT2);
			RAE.appendChild(RAN);
		}
		if(!(RA.getType() == null))
		{
			Element RAL = dom.createElement("Level");
			Text RT3 = dom.createTextNode(RA.getType());
			RAL.appendChild(RT3);
			RAE.appendChild(RAL);
		}
		if(!(RA.getUsername() == null))
		{		
			Element RAU = dom.createElement("Username");
			Text RT4 = dom.createTextNode(RA.getUsername());
			RAU.appendChild(RT4);
			RAE.appendChild(RAU);
		}
		
		return RAE;		
	}
	
	private Element createPathRuleElement(PathRule PR){
		Element PRE = dom.createElement("PathRule");
		PRE.setAttribute("Name", PR.getName());
		
		Element PE = dom.createElement("Pattern");
		Text PT = dom.createTextNode(PR.getPathPattern());
			
		PE.appendChild(PT);
		PRE.appendChild(PE);
		
		return PRE;	
	}
	
	private Element createDefectRuleElement(DefectRule DR){
		Element DRE = dom.createElement("DefectRule");
		DRE.setAttribute("Name", DR.getName());
		
		Element OE = dom.createElement("Owner");
		if(DR.getOwner() == null)
		{
			//Text DT = dom.createTextNode("null");
			//OE.appendChild(DT);
			//DRE.appendChild(OE);
		}
		else
		{
			Text DT = dom.createTextNode(DR.getOwner());
			OE.appendChild(DT);
			DRE.appendChild(OE);
		}
			
		return DRE;	
	}
	
	private Element createSubscriberElement(String S){
		Element SE = dom.createElement("Subscriber");
		SE.setAttribute("Name", S);
		//System.out.println("SUBSCRIBER: " + S);
		return SE;	
	}

	/**
	 * This method uses Xerces specific classes
	 * prints the XML document to file.
     */

	private void printToFile(){
	
		try
		{
			//print
			OutputFormat format = new OutputFormat(dom);
			format.setIndenting(true);
	
			//to generate output to console use this serializer
			//XMLSerializer serializer = new XMLSerializer(System.out, format);
	
	
			//to generate a file output use fileoutputstream instead of system.out
			XMLSerializer serializer = new XMLSerializer(
			new FileOutputStream(new File("cmaps.xml")), format);
	
			serializer.serialize(dom);
	
		} catch(IOException ie) {
		    ie.printStackTrace();
		}
	}
}

