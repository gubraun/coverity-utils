
package com.coverity.ws.v7;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for checkerPropertyDataObj complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="checkerPropertyDataObj">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="category" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="categoryDescription" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="checkerSubcategoryId" type="{http://ws.coverity.com/v7}checkerSubcategoryIdDataObj" minOccurs="0"/>
 *         &lt;element name="cweCategory" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="eventSetCaptions" type="{http://www.w3.org/2001/XMLSchema}string" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="impact" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="impactDescription" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="subcategoryLocalEffect" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="subcategoryLongDescription" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="subcategoryShortDescription" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "checkerPropertyDataObj", propOrder = {
    "category",
    "categoryDescription",
    "checkerSubcategoryId",
    "cweCategory",
    "eventSetCaptions",
    "impact",
    "impactDescription",
    "subcategoryLocalEffect",
    "subcategoryLongDescription",
    "subcategoryShortDescription"
})
public class CheckerPropertyDataObj {

    protected String category;
    protected String categoryDescription;
    protected CheckerSubcategoryIdDataObj checkerSubcategoryId;
    protected String cweCategory;
    @XmlElement(nillable = true)
    protected List<String> eventSetCaptions;
    protected String impact;
    protected String impactDescription;
    protected String subcategoryLocalEffect;
    protected String subcategoryLongDescription;
    protected String subcategoryShortDescription;

    /**
     * Gets the value of the category property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCategory() {
        return category;
    }

    /**
     * Sets the value of the category property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCategory(String value) {
        this.category = value;
    }

    /**
     * Gets the value of the categoryDescription property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCategoryDescription() {
        return categoryDescription;
    }

    /**
     * Sets the value of the categoryDescription property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCategoryDescription(String value) {
        this.categoryDescription = value;
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
     * Gets the value of the cweCategory property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCweCategory() {
        return cweCategory;
    }

    /**
     * Sets the value of the cweCategory property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCweCategory(String value) {
        this.cweCategory = value;
    }

    /**
     * Gets the value of the eventSetCaptions property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the eventSetCaptions property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getEventSetCaptions().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link String }
     * 
     * 
     */
    public List<String> getEventSetCaptions() {
        if (eventSetCaptions == null) {
            eventSetCaptions = new ArrayList<String>();
        }
        return this.eventSetCaptions;
    }

    /**
     * Gets the value of the impact property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getImpact() {
        return impact;
    }

    /**
     * Sets the value of the impact property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setImpact(String value) {
        this.impact = value;
    }

    /**
     * Gets the value of the impactDescription property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getImpactDescription() {
        return impactDescription;
    }

    /**
     * Sets the value of the impactDescription property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setImpactDescription(String value) {
        this.impactDescription = value;
    }

    /**
     * Gets the value of the subcategoryLocalEffect property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSubcategoryLocalEffect() {
        return subcategoryLocalEffect;
    }

    /**
     * Sets the value of the subcategoryLocalEffect property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSubcategoryLocalEffect(String value) {
        this.subcategoryLocalEffect = value;
    }

    /**
     * Gets the value of the subcategoryLongDescription property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSubcategoryLongDescription() {
        return subcategoryLongDescription;
    }

    /**
     * Sets the value of the subcategoryLongDescription property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSubcategoryLongDescription(String value) {
        this.subcategoryLongDescription = value;
    }

    /**
     * Gets the value of the subcategoryShortDescription property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSubcategoryShortDescription() {
        return subcategoryShortDescription;
    }

    /**
     * Sets the value of the subcategoryShortDescription property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSubcategoryShortDescription(String value) {
        this.subcategoryShortDescription = value;
    }

}
