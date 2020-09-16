// (c) 2009 Coverity, Inc. All rights reserved worldwide.

package CovComponents;

import javax.xml.ws.WebServiceRef;


//import java.awt.Component;
import java.net.URL;

import javax.xml.namespace.QName;
import javax.xml.ws.BindingProvider;
import javax.xml.ws.WebServiceException;
import javax.xml.ws.soap.SOAPFaultException;
import javax.xml.ws.handler.Handler;

import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

import com.coverity.ws.v8.*;

/**
 * This application reads all defined Component Maps from an XML file (exported via the ReadComponents utility)
 * and creates the component maps/components in a Coverity Connect instance.
 *
 */
public class covcomponents {
	static boolean mydebugflag=true;
	static boolean update=false;
	
    /**
     * <code>main</code> entry point.
     */
	public static void main (String[] args) {
		try {
			if(args.length != 3){
				System.err.println(
                    "Usage:\n <this-command> <server-address>:<port> <admin-password> <update/create>");
				System.exit(1);
			}
			covcomponents covComponents = new covcomponents();
			update = args[2].equalsIgnoreCase("update");
			covComponents.writeComponent(args[0], args[1]);
		}
		catch (Exception e){
			e.printStackTrace();
		}
	}

    /**     * Gets a list of assignable users from the target server address and writes
     * the list to standard output.
     *
     * @param serverAddr
     *          The address of the server, including the port number
     *          in <code>address:port</code> format.
     *
     * @param password
     *          The password for the "admin" user.
     */
	
	public void writeComponent(String serverAddr, String password)
    throws Exception {
    try {
        // Create a Web Services port to the server
        ConfigurationServiceService configurationServiceService =
            new ConfigurationServiceService(
                new URL("http://" + serverAddr + "/ws/v8/configurationservice?wsdl"),
                new QName("http://ws.coverity.com/v8", "ConfigurationServiceService"));
        ConfigurationService configurationService =
            configurationServiceService.getConfigurationServicePort();

        // Attach an authentication handler to it
        BindingProvider bindingProvider = (BindingProvider)configurationService;
        bindingProvider.getBinding().setHandlerChain(
            new ArrayList<Handler>(Arrays.asList(
               	new ClientAuthenticationHandlerWSS("admin", password))));

        //System.out.println("Creating List");
        // Create a Component Map List
        List<ComponentMap> componentMap = new ArrayList<ComponentMap>();
        
        System.out.println(" ");
        System.out.println("----------------------");
        System.out.println("PARSING FILE CMAPS.XML");
        System.out.println("----------------------");
        
        // Parse the XML File "cmaps.xml"
        parseXMLFile(componentMap);
        
        System.out.println(" ");
        System.out.println("------------------------");
        System.out.println("POPULATING COMPONENT MAP");
        System.out.println("------------------------");
        
        // Read in Component Map Data via XML and store in CIM Database
        populateComponentMap(configurationService, componentMap);
        
        System.out.println(" ");
        System.out.println("COMPLETE !!!");
        System.out.println(" ");   
       
      }
	  catch (SOAPFaultException x)
	  {
		  System.err.println(x);
	  }
	  catch (WebServiceException x)
	  {
		  System.err.println(x);
	  }
	
	}
	

	public void populateComponentMap(ConfigurationService configurationService, List<ComponentMap> componentMap)
	throws Exception {
		
		boolean needToUpdate=false;
		
	try { 
		// Iterate through each component map
	    for (int x = 0; x < componentMap.size(); x++)
	    {
	    	ComponentMap aCompMap = componentMap.get(x);
	    	
	    	// If the component map exists...then, determine if we want an update to occur, if not, continue
	    	needToUpdate = checkComponentMaps(configurationService, aCompMap.getCmapname());
	        	// Update	needToUpdate	s contains "Other"	Action
	        	// 	T			T				T				Create 'Other' component
	        	//	T			T				F				Create component
	        	//	T			F				T				Skip creating 'Other' component
	        	//	T			F				F				Create component
	        	// 	F			T				T				Skip component map altogether (not updating, only creating)
	        	//	F			T				F				Skip component map altogether (not updating, only creating)
	        	//	F			F				T				Skip creating 'Other' component
	        	//	F			F				F				Create component
	    	if ((!update) && (needToUpdate)) continue;
	        
	    	// Print the Component Map Name and Description
	    	System.out.println("MAP ==> DESCRIPTION: " + aCompMap.getCmapname() + " ==> " + aCompMap.getDescription());
	    	
	        // Create Component Map
	        ComponentMapSpecDataObj componentMapId = new ComponentMapSpecDataObj();

	        // Create Component Map Name
	        componentMapId.setComponentMapName(aCompMap.getCmapname());
	        componentMapId.setDescription(aCompMap.getDescription());
	                
	        System.out.println("SIZE: " +  aCompMap.getComponents().size());
	     
	        for (int i=0; i < aCompMap.getComponents().size(); i++)
	        {
	        	Component C = aCompMap.getComponents().get(i);
	        	
	        	String s = C.getName();
	        	String t = "Other";
	        	
	        	// See truth table above

	        	if (((!update) || (!needToUpdate)) && (s.contains(t))) continue;
	        
	        	// Create Component
				ComponentDataObj Comp1 = new ComponentDataObj();
	        
	        	// Create Component ID
				ComponentIdDataObj ID1 = new ComponentIdDataObj();	
	        
	        	// Component names should be map name scoped
				if (mydebugflag) System.out.println("Component Name: " + aCompMap.getCmapname() + "." + C.getName());
	        	ID1.setName(C.getName());
				Comp1.setComponentId(ID1);

				// Set Role Assignments
	        	for (int j=0; j < C.getRoleAssign().size(); j++)
	            {
	    			RoleAssignment RA = C.getRoleAssign().get(j);
	    		
	    			
		           	// Create the group Id object to be added
			        GroupIdDataObj groupId = new GroupIdDataObj();
			        groupId.setName(RA.getGid());
			        if (RA.getDomain() != null) {
			        	ServerDomainIdDataObj sDomain = new ServerDomainIdDataObj();			        	
			        	sDomain.setName(RA.getDomain());
			        	groupId.setDomain(sDomain);
			        }
        
		           	// Create the Role Id object to be added
			        RoleIdDataObj roleId = new RoleIdDataObj();
			        if (mydebugflag) System.out.println("Role Name: " + RA.getName());
			        roleId.setName(RA.getName());
			        		
			        // Create a Group Permisson
			        RoleAssignmentDataObj Role1 = new RoleAssignmentDataObj(); 	
			        Role1.setGroupId(groupId);
			        Role1.setRoleId(roleId);
			        Role1.setRoleAssignmentType(RA.getRtype());
			        Role1.setType(RA.getType());
			        Role1.setUsername(RA.getUsername());
			   
			        if (mydebugflag) System.out.println("Role Group ID: " + RA.getGid() + " Role:Name " + roleId.getName() + " Role:AssignmentType " + Role1.getRoleAssignmentType() + " Role:Type " + Role1.getType() + " Role:Username " + Role1.getUsername());
			        
			        //Add the list of permissions to the component
			        Comp1.getRoleAssignments().add(Role1);			        			        
			   	}
	      
	        	// Set Subscribers
			  	for (int k=0; k < C.getSubscribers().size(); k++)
	            {
	    			String S = C.getSubscribers().get(k);
	        		Comp1.getSubscribers().add(S);
	    			if (mydebugflag) System.out.println("Subscriber: " + S);
	            }
	           	// Add the component to the componentMap
		        componentMapId.getComponents().add(Comp1);
	        }
	        
	        // Add path rules
	        for (int i=0; i < aCompMap.getPathRules().size(); i++)
	        {
				PathRule PR = aCompMap.getPathRules().get(i);
			    ComponentPathRuleDataObj componentPath = new ComponentPathRuleDataObj();
		    
			    ComponentIdDataObj ID2 = new ComponentIdDataObj();	    
				ID2.setName(PR.getName());
    	        componentPath.setComponentId(ID2);
		        componentPath.setPathPattern(PR.getPathPattern());
	
		        // Add the component path to the component map
		        componentMapId.getComponentPathRules().add(componentPath);
		   }
	  
	        // Add defect rules
			for (int i=0; i < aCompMap.getDefectRules().size(); i++)
			{
				DefectRule DR = aCompMap.getDefectRules().get(i);
				ComponentDefectRuleDataObj componentDefect = new ComponentDefectRuleDataObj();

				ComponentIdDataObj ID3 = new ComponentIdDataObj();
				if (mydebugflag) System.out.println("Defect Rule: " + DR.getName());
				ID3.setName(DR.getName());
				componentDefect.setComponentId(ID3);
				componentDefect.setDefaultOwner(DR.getOwner());
				
				componentMapId.getDefectRules().add(componentDefect);
			}
     		

			if ((update) && (needToUpdate)) {
	        // Update the existing Component Map
				ComponentMapIdDataObj componentName = new ComponentMapIdDataObj();
				componentName.setName(aCompMap.getCmapname());
				configurationService.updateComponentMap(componentName, componentMapId);				
			} 
			else {
				//In update mode, but can't update because the Component Map doesn't currently exist, then add it
				//If not in update mode, then add it
				//The case of "not in update mode" and "needToUpdate" (Component Map currently exists in CoCo)
				//   is handled by logic at the top that does a 'continue', thus
				//   ignoring the component map
				configurationService.createComponentMap(componentMapId);
			}
	    }
	}
	catch (CovRemoteServiceException_Exception x)
	{
	    System.err.println(x);
	}
	catch (SOAPFaultException x)
	{
		System.err.println(x);
	}
	catch (WebServiceException x)
	{
		System.err.println(x);
	}
	
}

public void parseXMLFile(List<ComponentMap> componentMap)
{
	XMLLib xmllib = new XMLLib(componentMap);
	xmllib.runParseFile();
}

	// Returns TRUE if the specified Component Map already exists
	  private boolean checkComponentMaps(ConfigurationService cs, String compMapName){
	    try{  
	      ComponentMapFilterSpecDataObj componentMapId = new ComponentMapFilterSpecDataObj();
	      componentMapId.setNamePattern(compMapName);	      
	      List<ComponentMapDataObj> compMap = cs.getComponentMaps(componentMapId);
	  	
	      // For Each Component Map
		  for (ComponentMapDataObj aComp : compMap )
		  {
			  String s = aComp.getComponentMapId().getName();
			  
			  if(s.equals(compMapName))
				  return true;
		  }
		  
	    }
	    catch (CovRemoteServiceException_Exception x){
	      System.err.println(x);
	    }
	    catch (SOAPFaultException x){
	      System.err.println(x);
	    }
	    catch (WebServiceException x){
	      System.err.println(x);
	    }
	    return false;
	  }

}

