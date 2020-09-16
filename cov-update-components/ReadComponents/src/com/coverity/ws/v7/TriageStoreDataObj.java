
package com.coverity.ws.v7;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for triageStoreDataObj complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="triageStoreDataObj">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="description" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="id" type="{http://ws.coverity.com/v7}triageStoreIdDataObj" minOccurs="0"/>
 *         &lt;element name="streamIds" type="{http://ws.coverity.com/v7}streamIdDataObj" maxOccurs="unbounded" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "triageStoreDataObj", propOrder = {
    "description",
    "id",
    "streamIds"
})
public class TriageStoreDataObj {

    protected String description;
    protected TriageStoreIdDataObj id;
    @XmlElement(nillable = true)
    protected List<StreamIdDataObj> streamIds;

    /**
     * Gets the value of the description property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDescription() {
        return description;
    }

    /**
     * Sets the value of the description property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDescription(String value) {
        this.description = value;
    }

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link TriageStoreIdDataObj }
     *     
     */
    public TriageStoreIdDataObj getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link TriageStoreIdDataObj }
     *     
     */
    public void setId(TriageStoreIdDataObj value) {
        this.id = value;
    }

    /**
     * Gets the value of the streamIds property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the streamIds property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getStreamIds().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link StreamIdDataObj }
     * 
     * 
     */
    public List<StreamIdDataObj> getStreamIds() {
        if (streamIds == null) {
            streamIds = new ArrayList<StreamIdDataObj>();
        }
        return this.streamIds;
    }

}
