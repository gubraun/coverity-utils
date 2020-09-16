
package com.coverity.ws.v7;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for streamDefectDataObj complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="streamDefectDataObj">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="history" type="{http://ws.coverity.com/v7}defectStateDataObj" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="defectInstances" type="{http://ws.coverity.com/v7}defectInstanceDataObj" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="checkerSubcategoryId" type="{http://ws.coverity.com/v7}checkerSubcategoryIdDataObj" minOccurs="0"/>
 *         &lt;element name="cid" type="{http://www.w3.org/2001/XMLSchema}long" minOccurs="0"/>
 *         &lt;element name="defectStateAttributeValues" type="{http://ws.coverity.com/v7}defectStateAttributeValueDataObj" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="id" type="{http://ws.coverity.com/v7}streamDefectIdDataObj" minOccurs="0"/>
 *         &lt;element name="streamId" type="{http://ws.coverity.com/v7}streamIdDataObj" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "streamDefectDataObj", propOrder = {
    "history",
    "defectInstances",
    "checkerSubcategoryId",
    "cid",
    "defectStateAttributeValues",
    "id",
    "streamId"
})
public class StreamDefectDataObj {

    @XmlElement(nillable = true)
    protected List<DefectStateDataObj> history;
    @XmlElement(nillable = true)
    protected List<DefectInstanceDataObj> defectInstances;
    protected CheckerSubcategoryIdDataObj checkerSubcategoryId;
    protected Long cid;
    @XmlElement(nillable = true)
    protected List<DefectStateAttributeValueDataObj> defectStateAttributeValues;
    protected StreamDefectIdDataObj id;
    protected StreamIdDataObj streamId;

    /**
     * Gets the value of the history property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the history property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getHistory().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link DefectStateDataObj }
     * 
     * 
     */
    public List<DefectStateDataObj> getHistory() {
        if (history == null) {
            history = new ArrayList<DefectStateDataObj>();
        }
        return this.history;
    }

    /**
     * Gets the value of the defectInstances property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the defectInstances property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getDefectInstances().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link DefectInstanceDataObj }
     * 
     * 
     */
    public List<DefectInstanceDataObj> getDefectInstances() {
        if (defectInstances == null) {
            defectInstances = new ArrayList<DefectInstanceDataObj>();
        }
        return this.defectInstances;
    }

    /**
     * Gets the value of the checkerSubcategoryId property.
     * 
     * @return
     *     possible object is
     *     {@link CheckerSubcategoryIdDataObj }
     *     
     */
    public CheckerSubcategoryIdDataObj getCheckerSubcategoryId() {
        return checkerSubcategoryId;
    }

    /**
     * Sets the value of the checkerSubcategoryId property.
     * 
     * @param value
     *     allowed object is
     *     {@link CheckerSubcategoryIdDataObj }
     *     
     */
    public void setCheckerSubcategoryId(CheckerSubcategoryIdDataObj value) {
        this.checkerSubcategoryId = value;
    }

    /**
     * Gets the value of the cid property.
     * 
     * @return
     *     possible object is
     *     {@link Long }
     *     
     */
    public Long getCid() {
        return cid;
    }

    /**
     * Sets the value of the cid property.
     * 
     * @param value
     *     allowed object is
     *     {@link Long }
     *     
     */
    public void setCid(Long value) {
        this.cid = value;
    }

    /**
     * Gets the value of the defectStateAttributeValues property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the defectStateAttributeValues property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getDefectStateAttributeValues().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link DefectStateAttributeValueDataObj }
     * 
     * 
     */
    public List<DefectStateAttributeValueDataObj> getDefectStateAttributeValues() {
        if (defectStateAttributeValues == null) {
            defectStateAttributeValues = new ArrayList<DefectStateAttributeValueDataObj>();
        }
        return this.defectStateAttributeValues;
    }

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link StreamDefectIdDataObj }
     *     
     */
    public StreamDefectIdDataObj getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link StreamDefectIdDataObj }
     *     
     */
    public void setId(StreamDefectIdDataObj value) {
        this.id = value;
    }

    /**
     * Gets the value of the streamId property.
     * 
     * @return
     *     possible object is
     *     {@link StreamIdDataObj }
     *     
     */
    public StreamIdDataObj getStreamId() {
        return streamId;
    }

    /**
     * Sets the value of the streamId property.
     * 
     * @param value
     *     allowed object is
     *     {@link StreamIdDataObj }
     *     
     */
    public void setStreamId(StreamIdDataObj value) {
        this.streamId = value;
    }

}
