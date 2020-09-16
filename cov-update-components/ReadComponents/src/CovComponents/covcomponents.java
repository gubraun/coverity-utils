// (c) 2009 Coverity, Inc. All rights reserved worldwide.

package CovComponents;

import java.net.URL;
import javax.xml.namespace.QName;
import javax.xml.ws.BindingProvider;
import javax.xml.ws.WebServiceException;
import javax.xml.ws.soap.SOAPFaultException;
import javax.xml.ws.handler.Handler;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

//import CovComponents.*;
import com.coverity.ws.v7.*;

//import CovComponents.Component;

/**
 * This application reads all defined Component Maps in a Coverity Connect instance and writes the component maps into an XML file.  This file can then be transported
 * to another Coverity Connect server and the WriteComponents utility can be used to import the Component Maps and Components described in the XML file into the new
 * database.
 *
 */
public class covcomponents {
    /**
     * <code>main</code> entry point.
     */
	boolean mydebugflag=true;
	
	public static void main (String[] args) {
		try {
			if(args.length != 2){
				System.err.println(
                    "Usage:\n <this-command> <server-address>:<port> <admin-password>");
				System.exit(1);
			}
			covcomponents componentMaps = new covcomponents();
			componentMaps.exportComponentMaps(args[0], args[1]);
		}
		catch (Exception e){
			e.printStackTrace();
		}
	}

    /**
     * Gets a the Component Map/Components from the specified Coverity Connect database
     *
     * @param serverAddr
     *          The address of the server, including the port number
     *          in <code>address:port</code> format.
     *
     * @param password
     *          The password for the "admin" user.
     */
	public void exportComponentMaps(String serverAddr, String password)
        throws Exception {
        try {
           
            ConfigurationServiceService configurationServiceService =
                new ConfigurationServiceService(
                    new URL("http://" + serverAddr + "/ws/v7/configurationservice?wsdl"),
                    new QName("http://ws.coverity.com/v7", "ConfigurationServiceService"));
            ConfigurationService configurationService =
                configurationServiceService.getConfigurationServicePort();

            // Attach an authentication handler to it
            BindingProvider bindingProvider = (BindingProvider)configurationService;
            bindingProvider.getBinding().setHandlerChain(
                new ArrayList<Handler>(Arrays.asList(
                    new ClientAuthenticationHandlerWSS("admin", password))));

            // Create a Component Map List
            List<ComponentMap> componentMap = new ArrayList<ComponentMap>();
            
            System.out.println(" ");
            System.out.println("---------------------------");
            System.out.println("READING COMPONENTS FROM CIM");
            System.out.println("---------------------------");
                        
            // Read in Component Map Data via Web Services and store in List
            populateComponentMap(configurationService, componentMap);
            /*
            for(int i=0; i < componentMap.size(); i++)
            {
            	System.out.println(componentMap.get(i).getCmapname());
            }   
            */       
            
            // Create an XML File from the stored List
            createXMLFile(componentMap);
                      
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
	
	public void populateComponentMap(ConfigurationService configurationService, List<ComponentMap> componentMap)
		throws Exception {
		try {
			  int i=0;
			  ComponentMapFilterSpecDataObj componentMapId = new ComponentMapFilterSpecDataObj();
	          componentMapId.setNamePattern("*");
	          List<ComponentMapDataObj> compMap = configurationService.getComponentMaps(componentMapId);
	
		        // For Each Component Map
			    for (ComponentMapDataObj aComp : compMap )
			    {		    	
 			    	//System.out.println(" ");
			    	// Print the Component Map Name and Description
			    	System.out.println("MAP ==> DESCRIPTION: " + aComp.getComponentMapId().getName() +
			    			" ==> " + aComp.getDescription());
		
			    	// Create Component Map
			    	ComponentMap localComponentMap = new ComponentMap(aComp.getComponentMapId().getName(), aComp.getDescription());
			    				    	
			    	// Get Component Name + Subscribers + Permissions
			    	for(ComponentDataObj aData : aComp.getComponents())
			    	{
		   		   		if(mydebugflag) System.out.println("COMPONENT: " + aData.getComponentId().getName());
		   		   		
		   		   		Component localComponent = new Component(aData.getComponentId().getName());
		        
		   		   		for(String S : aData.getSubscribers())
		   		   		{
		   		   			if(mydebugflag) System.out.println("SUBSCRIBER: " + S);
		   		   			localComponent.setSubscriber(S);
		                }
		   		   		
		   		  		for(RoleAssignmentDataObj aRole : aData.getRoleAssignments())
		   		   		{	
		   		  			// It is possible that the Role is assigned to an individual, not to a Group, therefore GroupId would be null
		   		  			// And there would be no Domain associated with the Role.
		   		  			// Therefore, the Role Assignment would be for an individual
		   		  			if (aRole.getGroupId() == null) {
		   		  				
		   		  				RoleAssignment localRoleAssign = new RoleAssignment(aRole.getRoleId().getName());
			   		  				   		  				
		   		   			    if(mydebugflag) System.out.println("ROLE ASSIGNMENT Name: " + aRole.getRoleId().getName());
		   		   			    localRoleAssign.setName(aRole.getRoleId().getName());
		   		   			    //System.out.println("N: " + localRoleAssign.getName());
		   		   			    		   		   			
			   		   			if(mydebugflag) System.out.println("ROLE ASSIGNMENT Role Assignment Type: " + aRole.getRoleAssignmentType());
			   		   			localRoleAssign.setRtype(aRole.getRoleAssignmentType());
			   		   			//System.out.println("RT: " + localRoleAssign.getRtype());
			   		   			   		   					   		   			   		   		   		   			
			   		   			if(mydebugflag) System.out.println("ROLE ASSIGNMENT Type/Level: " + aRole.getType());
			   		   			localRoleAssign.setType(aRole.getType());
			   		   			//System.out.println("T: " + localRoleAssign.getType());
			   		   					   		   			
			   		   			if(mydebugflag) System.out.println("ROLE ASSIGNMENT Username: " + aRole.getUsername());
			   		   			localRoleAssign.setUsername(aRole.getUsername());
			   		   			//System.out.println("UN: " + localRoleAssign.getUsername());
			   		   			
			   		   			localComponent.setRoleAssign(localRoleAssign);
		   		  			} else {
		   		  				// Role Assignment is for a Group
			   		  			if(mydebugflag) System.out.println("ROLE ASSIGNMENT Group: " + aRole.getGroupId().getName());
			   		  			RoleAssignment localRoleAssign = new RoleAssignment(aRole.getGroupId().getName());
			   		  			
			   		  			ServerDomainIdDataObj sDomain = aRole.getGroupId().getDomain();
			   		  			
			   		  			if(sDomain == null)
			   		  			{
			   		  				if(mydebugflag) System.out.println("NULL");
			   		  				localRoleAssign.setDomain(null);
			   		  			}		   		  			
			   		  			else
			   		  			{
			   		  				if(mydebugflag) System.out.println("GOT DOMAIN");
			   		  				localRoleAssign.setDomain(sDomain.getName());
			   		  			}
		   		  			
		   		   			    if(mydebugflag) System.out.println("ROLE ASSIGNMENT Name: " + aRole.getRoleId().getName());
		   		   			    localRoleAssign.setName(aRole.getRoleId().getName());
		   		   			    //System.out.println("N: " + localRoleAssign.getName());
		   		   			    		   		   			
			   		   			if(mydebugflag) System.out.println("ROLE ASSIGNMENT Role Assignment Type: " + aRole.getRoleAssignmentType());
			   		   			localRoleAssign.setRtype(aRole.getRoleAssignmentType());
			   		   			//System.out.println("RT: " + localRoleAssign.getRtype());
			   		   			   		   					   		   			   		   		   		   			
			   		   			if(mydebugflag) System.out.println("ROLE ASSIGNMENT Type/Level: " + aRole.getType());
			   		   			localRoleAssign.setType(aRole.getType());
			   		   			//System.out.println("T: " + localRoleAssign.getType());
			   		   					   		   			
			   		   			if(mydebugflag) System.out.println("ROLE ASSIGNMENT Username: " + aRole.getUsername());
			   		   			localRoleAssign.setUsername(aRole.getUsername());
			   		   			//System.out.println("UN: " + localRoleAssign.getUsername());
			   		   			
			   		   			localComponent.setRoleAssign(localRoleAssign);
		   		  			}
		   		   		}
		             
		   		   		localComponentMap.setComponent(localComponent);
		            }
			   			    			
			    	// Get ComponentId Name and Path Pattern for each component
			    	for(ComponentPathRuleDataObj aRule : aComp.getComponentPathRules())
			    	{
			    		PathRule localPathRule = new PathRule(aRule.getComponentId().getName());
			    		
			    		if(mydebugflag) System.out.println("COMP_ID ==> REGEX: " + aRule.getComponentId().getName() +
			    				" ==> " + aRule.getPathPattern());
			    		
			    		localPathRule.setPathPattern(aRule.getPathPattern());			    		
			    		localComponentMap.setPathRule(localPathRule);
			    	}
			    	
			    	// Get Defect Rules for each component
			    	for(ComponentDefectRuleDataObj aDefect : aComp.getDefectRules())
			    	{
			    		DefectRule localDefectRule = new DefectRule(aDefect.getComponentId().getName());
			    		
			    		if(mydebugflag) System.out.println("COMP_ID ==> DEFAULT OWNER: " + aDefect.getComponentId().getName() +
			    				" ==> " + aDefect.getDefaultOwner());
			    		
			    		localDefectRule.setOwner(aDefect.getDefaultOwner());
			    		localComponentMap.setDefectRule(localDefectRule);
			    	}
			    	
			    	componentMap.add(localComponentMap);
		
			    	if(mydebugflag) System.out.println("**************************");
			    	if(mydebugflag) System.out.println(componentMap.get(i).getCmapname() + ": " + (i+1));
			    	if(mydebugflag) System.out.println("**************************");
			    	i++;
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
	
	public void createXMLFile(List<ComponentMap> componentMap)
	{
		XMLLib xmllib = new XMLLib(componentMap);
		
		//System.out.println("Before");
		xmllib.runCreateFile();
		//System.out.println("After");
	}
	
}