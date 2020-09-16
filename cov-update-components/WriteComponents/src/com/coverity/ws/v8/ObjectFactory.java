
package com.coverity.ws.v8;

import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlElementDecl;
import javax.xml.bind.annotation.XmlRegistry;
import javax.xml.namespace.QName;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the com.coverity.ws.v8 package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {

    private final static QName _GetCheckerSubcategoriesForProjectResponse_QNAME = new QName("http://ws.coverity.com/v8", "getCheckerSubcategoriesForProjectResponse");
    private final static QName _GetComponentMetricsForProject_QNAME = new QName("http://ws.coverity.com/v8", "getComponentMetricsForProject");
    private final static QName _GetCheckerSubcategoriesForStreamsResponse_QNAME = new QName("http://ws.coverity.com/v8", "getCheckerSubcategoriesForStreamsResponse");
    private final static QName _UpdateDefectInstancePropertiesResponse_QNAME = new QName("http://ws.coverity.com/v8", "updateDefectInstancePropertiesResponse");
    private final static QName _UpdateDefectInstanceProperties_QNAME = new QName("http://ws.coverity.com/v8", "updateDefectInstanceProperties");
    private final static QName _GetMergedDefectsForStreamsResponse_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectsForStreamsResponse");
    private final static QName _UpdateTriageForCIDsInTriageStore_QNAME = new QName("http://ws.coverity.com/v8", "updateTriageForCIDsInTriageStore");
    private final static QName _GetFileContents_QNAME = new QName("http://ws.coverity.com/v8", "getFileContents");
    private final static QName _CoverityFault_QNAME = new QName("http://ws.coverity.com/v8", "CoverityFault");
    private final static QName _CreateMergedDefectResponse_QNAME = new QName("http://ws.coverity.com/v8", "createMergedDefectResponse");
    private final static QName _GetMergedDefectsForSnapshotScope_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectsForSnapshotScope");
    private final static QName _GetMergedDefectHistoryResponse_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectHistoryResponse");
    private final static QName _UpdateStreamDefects_QNAME = new QName("http://ws.coverity.com/v8", "updateStreamDefects");
    private final static QName _GetCheckerSubcategoriesForProject_QNAME = new QName("http://ws.coverity.com/v8", "getCheckerSubcategoriesForProject");
    private final static QName _GetComponentMetricsForProjectResponse_QNAME = new QName("http://ws.coverity.com/v8", "getComponentMetricsForProjectResponse");
    private final static QName _GetTrendRecordsForProjectResponse_QNAME = new QName("http://ws.coverity.com/v8", "getTrendRecordsForProjectResponse");
    private final static QName _GetStreamDefects_QNAME = new QName("http://ws.coverity.com/v8", "getStreamDefects");
    private final static QName _GetStreamDefectsResponse_QNAME = new QName("http://ws.coverity.com/v8", "getStreamDefectsResponse");
    private final static QName _UpdateStreamDefectsResponse_QNAME = new QName("http://ws.coverity.com/v8", "updateStreamDefectsResponse");
    private final static QName _GetMergedDefectsForProjectScope_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectsForProjectScope");
    private final static QName _GetMergedDefectsForProjectScopeResponse_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectsForProjectScopeResponse");
    private final static QName _UpdateTriageForCIDsInTriageStoreResponse_QNAME = new QName("http://ws.coverity.com/v8", "updateTriageForCIDsInTriageStoreResponse");
    private final static QName _GetFileContentsResponse_QNAME = new QName("http://ws.coverity.com/v8", "getFileContentsResponse");
    private final static QName _GetTriageHistory_QNAME = new QName("http://ws.coverity.com/v8", "getTriageHistory");
    private final static QName _GetMergedDefectDetectionHistory_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectDetectionHistory");
    private final static QName _GetTrendRecordsForProject_QNAME = new QName("http://ws.coverity.com/v8", "getTrendRecordsForProject");
    private final static QName _GetMergedDefectsForSnapshotScopeResponse_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectsForSnapshotScopeResponse");
    private final static QName _GetTriageHistoryResponse_QNAME = new QName("http://ws.coverity.com/v8", "getTriageHistoryResponse");
    private final static QName _GetMergedDefectDetectionHistoryResponse_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectDetectionHistoryResponse");
    private final static QName _GetMergedDefectsForStreams_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectsForStreams");
    private final static QName _CreateMergedDefect_QNAME = new QName("http://ws.coverity.com/v8", "createMergedDefect");
    private final static QName _GetMergedDefectHistory_QNAME = new QName("http://ws.coverity.com/v8", "getMergedDefectHistory");
    private final static QName _GetCheckerSubcategoriesForStreams_QNAME = new QName("http://ws.coverity.com/v8", "getCheckerSubcategoriesForStreams");

    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: com.coverity.ws.v8
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link GetTriageHistoryResponse }
     * 
     */
    public GetTriageHistoryResponse createGetTriageHistoryResponse() {
        return new GetTriageHistoryResponse();
    }

    /**
     * Create an instance of {@link GetMergedDefectsForSnapshotScopeResponse }
     * 
     */
    public GetMergedDefectsForSnapshotScopeResponse createGetMergedDefectsForSnapshotScopeResponse() {
        return new GetMergedDefectsForSnapshotScopeResponse();
    }

    /**
     * Create an instance of {@link GetMergedDefectHistory }
     * 
     */
    public GetMergedDefectHistory createGetMergedDefectHistory() {
        return new GetMergedDefectHistory();
    }

    /**
     * Create an instance of {@link GetCheckerSubcategoriesForStreams }
     * 
     */
    public GetCheckerSubcategoriesForStreams createGetCheckerSubcategoriesForStreams() {
        return new GetCheckerSubcategoriesForStreams();
    }

    /**
     * Create an instance of {@link GetMergedDefectsForStreams }
     * 
     */
    public GetMergedDefectsForStreams createGetMergedDefectsForStreams() {
        return new GetMergedDefectsForStreams();
    }

    /**
     * Create an instance of {@link CreateMergedDefect }
     * 
     */
    public CreateMergedDefect createCreateMergedDefect() {
        return new CreateMergedDefect();
    }

    /**
     * Create an instance of {@link GetMergedDefectDetectionHistoryResponse }
     * 
     */
    public GetMergedDefectDetectionHistoryResponse createGetMergedDefectDetectionHistoryResponse() {
        return new GetMergedDefectDetectionHistoryResponse();
    }

    /**
     * Create an instance of {@link GetTriageHistory }
     * 
     */
    public GetTriageHistory createGetTriageHistory() {
        return new GetTriageHistory();
    }

    /**
     * Create an instance of {@link GetFileContentsResponse }
     * 
     */
    public GetFileContentsResponse createGetFileContentsResponse() {
        return new GetFileContentsResponse();
    }

    /**
     * Create an instance of {@link GetTrendRecordsForProject }
     * 
     */
    public GetTrendRecordsForProject createGetTrendRecordsForProject() {
        return new GetTrendRecordsForProject();
    }

    /**
     * Create an instance of {@link GetMergedDefectDetectionHistory }
     * 
     */
    public GetMergedDefectDetectionHistory createGetMergedDefectDetectionHistory() {
        return new GetMergedDefectDetectionHistory();
    }

    /**
     * Create an instance of {@link UpdateStreamDefectsResponse }
     * 
     */
    public UpdateStreamDefectsResponse createUpdateStreamDefectsResponse() {
        return new UpdateStreamDefectsResponse();
    }

    /**
     * Create an instance of {@link GetMergedDefectsForProjectScope }
     * 
     */
    public GetMergedDefectsForProjectScope createGetMergedDefectsForProjectScope() {
        return new GetMergedDefectsForProjectScope();
    }

    /**
     * Create an instance of {@link GetStreamDefectsResponse }
     * 
     */
    public GetStreamDefectsResponse createGetStreamDefectsResponse() {
        return new GetStreamDefectsResponse();
    }

    /**
     * Create an instance of {@link GetStreamDefects }
     * 
     */
    public GetStreamDefects createGetStreamDefects() {
        return new GetStreamDefects();
    }

    /**
     * Create an instance of {@link UpdateTriageForCIDsInTriageStoreResponse }
     * 
     */
    public UpdateTriageForCIDsInTriageStoreResponse createUpdateTriageForCIDsInTriageStoreResponse() {
        return new UpdateTriageForCIDsInTriageStoreResponse();
    }

    /**
     * Create an instance of {@link GetMergedDefectsForProjectScopeResponse }
     * 
     */
    public GetMergedDefectsForProjectScopeResponse createGetMergedDefectsForProjectScopeResponse() {
        return new GetMergedDefectsForProjectScopeResponse();
    }

    /**
     * Create an instance of {@link UpdateTriageForCIDsInTriageStore }
     * 
     */
    public UpdateTriageForCIDsInTriageStore createUpdateTriageForCIDsInTriageStore() {
        return new UpdateTriageForCIDsInTriageStore();
    }

    /**
     * Create an instance of {@link GetFileContents }
     * 
     */
    public GetFileContents createGetFileContents() {
        return new GetFileContents();
    }

    /**
     * Create an instance of {@link GetComponentMetricsForProject }
     * 
     */
    public GetComponentMetricsForProject createGetComponentMetricsForProject() {
        return new GetComponentMetricsForProject();
    }

    /**
     * Create an instance of {@link GetCheckerSubcategoriesForStreamsResponse }
     * 
     */
    public GetCheckerSubcategoriesForStreamsResponse createGetCheckerSubcategoriesForStreamsResponse() {
        return new GetCheckerSubcategoriesForStreamsResponse();
    }

    /**
     * Create an instance of {@link UpdateDefectInstancePropertiesResponse }
     * 
     */
    public UpdateDefectInstancePropertiesResponse createUpdateDefectInstancePropertiesResponse() {
        return new UpdateDefectInstancePropertiesResponse();
    }

    /**
     * Create an instance of {@link UpdateDefectInstanceProperties }
     * 
     */
    public UpdateDefectInstanceProperties createUpdateDefectInstanceProperties() {
        return new UpdateDefectInstanceProperties();
    }

    /**
     * Create an instance of {@link GetMergedDefectsForStreamsResponse }
     * 
     */
    public GetMergedDefectsForStreamsResponse createGetMergedDefectsForStreamsResponse() {
        return new GetMergedDefectsForStreamsResponse();
    }

    /**
     * Create an instance of {@link GetCheckerSubcategoriesForProjectResponse }
     * 
     */
    public GetCheckerSubcategoriesForProjectResponse createGetCheckerSubcategoriesForProjectResponse() {
        return new GetCheckerSubcategoriesForProjectResponse();
    }

    /**
     * Create an instance of {@link GetTrendRecordsForProjectResponse }
     * 
     */
    public GetTrendRecordsForProjectResponse createGetTrendRecordsForProjectResponse() {
        return new GetTrendRecordsForProjectResponse();
    }

    /**
     * Create an instance of {@link GetComponentMetricsForProjectResponse }
     * 
     */
    public GetComponentMetricsForProjectResponse createGetComponentMetricsForProjectResponse() {
        return new GetComponentMetricsForProjectResponse();
    }

    /**
     * Create an instance of {@link UpdateStreamDefects }
     * 
     */
    public UpdateStreamDefects createUpdateStreamDefects() {
        return new UpdateStreamDefects();
    }

    /**
     * Create an instance of {@link GetMergedDefectHistoryResponse }
     * 
     */
    public GetMergedDefectHistoryResponse createGetMergedDefectHistoryResponse() {
        return new GetMergedDefectHistoryResponse();
    }

    /**
     * Create an instance of {@link GetCheckerSubcategoriesForProject }
     * 
     */
    public GetCheckerSubcategoriesForProject createGetCheckerSubcategoriesForProject() {
        return new GetCheckerSubcategoriesForProject();
    }

    /**
     * Create an instance of {@link CreateMergedDefectResponse }
     * 
     */
    public CreateMergedDefectResponse createCreateMergedDefectResponse() {
        return new CreateMergedDefectResponse();
    }

    /**
     * Create an instance of {@link CovRemoteServiceException }
     * 
     */
    public CovRemoteServiceException createCovRemoteServiceException() {
        return new CovRemoteServiceException();
    }

    /**
     * Create an instance of {@link GetMergedDefectsForSnapshotScope }
     * 
     */
    public GetMergedDefectsForSnapshotScope createGetMergedDefectsForSnapshotScope() {
        return new GetMergedDefectsForSnapshotScope();
    }

    /**
     * Create an instance of {@link AttributeValueIdDataObj }
     * 
     */
    public AttributeValueIdDataObj createAttributeValueIdDataObj() {
        return new AttributeValueIdDataObj();
    }

    /**
     * Create an instance of {@link StreamDefectDataObj }
     * 
     */
    public StreamDefectDataObj createStreamDefectDataObj() {
        return new StreamDefectDataObj();
    }

    /**
     * Create an instance of {@link ProjectScopeDefectFilterSpecDataObj }
     * 
     */
    public ProjectScopeDefectFilterSpecDataObj createProjectScopeDefectFilterSpecDataObj() {
        return new ProjectScopeDefectFilterSpecDataObj();
    }

    /**
     * Create an instance of {@link SnapshotScopeDefectFilterSpecDataObj }
     * 
     */
    public SnapshotScopeDefectFilterSpecDataObj createSnapshotScopeDefectFilterSpecDataObj() {
        return new SnapshotScopeDefectFilterSpecDataObj();
    }

    /**
     * Create an instance of {@link FieldChangeDataObj }
     * 
     */
    public FieldChangeDataObj createFieldChangeDataObj() {
        return new FieldChangeDataObj();
    }

    /**
     * Create an instance of {@link SnapshotScopeSpecDataObj }
     * 
     */
    public SnapshotScopeSpecDataObj createSnapshotScopeSpecDataObj() {
        return new SnapshotScopeSpecDataObj();
    }

    /**
     * Create an instance of {@link ProjectTrendRecordFilterSpecDataObj }
     * 
     */
    public ProjectTrendRecordFilterSpecDataObj createProjectTrendRecordFilterSpecDataObj() {
        return new ProjectTrendRecordFilterSpecDataObj();
    }

    /**
     * Create an instance of {@link MergedDefectFilterSpecDataObj }
     * 
     */
    public MergedDefectFilterSpecDataObj createMergedDefectFilterSpecDataObj() {
        return new MergedDefectFilterSpecDataObj();
    }

    /**
     * Create an instance of {@link StreamDefectIdDataObj }
     * 
     */
    public StreamDefectIdDataObj createStreamDefectIdDataObj() {
        return new StreamDefectIdDataObj();
    }

    /**
     * Create an instance of {@link MergedDefectDataObj }
     * 
     */
    public MergedDefectDataObj createMergedDefectDataObj() {
        return new MergedDefectDataObj();
    }

    /**
     * Create an instance of {@link ProjectIdDataObj }
     * 
     */
    public ProjectIdDataObj createProjectIdDataObj() {
        return new ProjectIdDataObj();
    }

    /**
     * Create an instance of {@link DefectDetectionHistoryDataObj }
     * 
     */
    public DefectDetectionHistoryDataObj createDefectDetectionHistoryDataObj() {
        return new DefectDetectionHistoryDataObj();
    }

    /**
     * Create an instance of {@link CheckerSubcategoryIdDataObj }
     * 
     */
    public CheckerSubcategoryIdDataObj createCheckerSubcategoryIdDataObj() {
        return new CheckerSubcategoryIdDataObj();
    }

    /**
     * Create an instance of {@link DefectStateSpecDataObj }
     * 
     */
    public DefectStateSpecDataObj createDefectStateSpecDataObj() {
        return new DefectStateSpecDataObj();
    }

    /**
     * Create an instance of {@link DefectStateAttributeValueDataObj }
     * 
     */
    public DefectStateAttributeValueDataObj createDefectStateAttributeValueDataObj() {
        return new DefectStateAttributeValueDataObj();
    }

    /**
     * Create an instance of {@link EventDataObj }
     * 
     */
    public EventDataObj createEventDataObj() {
        return new EventDataObj();
    }

    /**
     * Create an instance of {@link StreamDefectFilterSpecDataObj }
     * 
     */
    public StreamDefectFilterSpecDataObj createStreamDefectFilterSpecDataObj() {
        return new StreamDefectFilterSpecDataObj();
    }

    /**
     * Create an instance of {@link PropertySpecDataObj }
     * 
     */
    public PropertySpecDataObj createPropertySpecDataObj() {
        return new PropertySpecDataObj();
    }

    /**
     * Create an instance of {@link MergedDefectsPageDataObj }
     * 
     */
    public MergedDefectsPageDataObj createMergedDefectsPageDataObj() {
        return new MergedDefectsPageDataObj();
    }

    /**
     * Create an instance of {@link FileContentsDataObj }
     * 
     */
    public FileContentsDataObj createFileContentsDataObj() {
        return new FileContentsDataObj();
    }

    /**
     * Create an instance of {@link ComponentMetricsDataObj }
     * 
     */
    public ComponentMetricsDataObj createComponentMetricsDataObj() {
        return new ComponentMetricsDataObj();
    }

    /**
     * Create an instance of {@link TriageHistoryDataObj }
     * 
     */
    public TriageHistoryDataObj createTriageHistoryDataObj() {
        return new TriageHistoryDataObj();
    }

    /**
     * Create an instance of {@link DefectChangeDataObj }
     * 
     */
    public DefectChangeDataObj createDefectChangeDataObj() {
        return new DefectChangeDataObj();
    }

    /**
     * Create an instance of {@link AttributeDefinitionIdDataObj }
     * 
     */
    public AttributeDefinitionIdDataObj createAttributeDefinitionIdDataObj() {
        return new AttributeDefinitionIdDataObj();
    }

    /**
     * Create an instance of {@link TriageStoreIdDataObj }
     * 
     */
    public TriageStoreIdDataObj createTriageStoreIdDataObj() {
        return new TriageStoreIdDataObj();
    }

    /**
     * Create an instance of {@link FileIdDataObj }
     * 
     */
    public FileIdDataObj createFileIdDataObj() {
        return new FileIdDataObj();
    }

    /**
     * Create an instance of {@link DefectStateDataObj }
     * 
     */
    public DefectStateDataObj createDefectStateDataObj() {
        return new DefectStateDataObj();
    }

    /**
     * Create an instance of {@link AttributeDefinitionValueFilterMapDataObj }
     * 
     */
    public AttributeDefinitionValueFilterMapDataObj createAttributeDefinitionValueFilterMapDataObj() {
        return new AttributeDefinitionValueFilterMapDataObj();
    }

    /**
     * Create an instance of {@link DefectInstanceIdDataObj }
     * 
     */
    public DefectInstanceIdDataObj createDefectInstanceIdDataObj() {
        return new DefectInstanceIdDataObj();
    }

    /**
     * Create an instance of {@link PageSpecDataObj }
     * 
     */
    public PageSpecDataObj createPageSpecDataObj() {
        return new PageSpecDataObj();
    }

    /**
     * Create an instance of {@link ProjectMetricsDataObj }
     * 
     */
    public ProjectMetricsDataObj createProjectMetricsDataObj() {
        return new ProjectMetricsDataObj();
    }

    /**
     * Create an instance of {@link DefectInstanceDataObj }
     * 
     */
    public DefectInstanceDataObj createDefectInstanceDataObj() {
        return new DefectInstanceDataObj();
    }

    /**
     * Create an instance of {@link StreamIdDataObj }
     * 
     */
    public StreamIdDataObj createStreamIdDataObj() {
        return new StreamIdDataObj();
    }

    /**
     * Create an instance of {@link FunctionInfoDataObj }
     * 
     */
    public FunctionInfoDataObj createFunctionInfoDataObj() {
        return new FunctionInfoDataObj();
    }

    /**
     * Create an instance of {@link CheckerSubcategoryFilterSpecDataObj }
     * 
     */
    public CheckerSubcategoryFilterSpecDataObj createCheckerSubcategoryFilterSpecDataObj() {
        return new CheckerSubcategoryFilterSpecDataObj();
    }

    /**
     * Create an instance of {@link ComponentIdDataObj }
     * 
     */
    public ComponentIdDataObj createComponentIdDataObj() {
        return new ComponentIdDataObj();
    }

    /**
     * Create an instance of {@link PropertyDataObj }
     * 
     */
    public PropertyDataObj createPropertyDataObj() {
        return new PropertyDataObj();
    }

    /**
     * Create an instance of {@link MergedDefectIdDataObj }
     * 
     */
    public MergedDefectIdDataObj createMergedDefectIdDataObj() {
        return new MergedDefectIdDataObj();
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetCheckerSubcategoriesForProjectResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getCheckerSubcategoriesForProjectResponse")
    public JAXBElement<GetCheckerSubcategoriesForProjectResponse> createGetCheckerSubcategoriesForProjectResponse(GetCheckerSubcategoriesForProjectResponse value) {
        return new JAXBElement<GetCheckerSubcategoriesForProjectResponse>(_GetCheckerSubcategoriesForProjectResponse_QNAME, GetCheckerSubcategoriesForProjectResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetComponentMetricsForProject }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getComponentMetricsForProject")
    public JAXBElement<GetComponentMetricsForProject> createGetComponentMetricsForProject(GetComponentMetricsForProject value) {
        return new JAXBElement<GetComponentMetricsForProject>(_GetComponentMetricsForProject_QNAME, GetComponentMetricsForProject.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetCheckerSubcategoriesForStreamsResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getCheckerSubcategoriesForStreamsResponse")
    public JAXBElement<GetCheckerSubcategoriesForStreamsResponse> createGetCheckerSubcategoriesForStreamsResponse(GetCheckerSubcategoriesForStreamsResponse value) {
        return new JAXBElement<GetCheckerSubcategoriesForStreamsResponse>(_GetCheckerSubcategoriesForStreamsResponse_QNAME, GetCheckerSubcategoriesForStreamsResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link UpdateDefectInstancePropertiesResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "updateDefectInstancePropertiesResponse")
    public JAXBElement<UpdateDefectInstancePropertiesResponse> createUpdateDefectInstancePropertiesResponse(UpdateDefectInstancePropertiesResponse value) {
        return new JAXBElement<UpdateDefectInstancePropertiesResponse>(_UpdateDefectInstancePropertiesResponse_QNAME, UpdateDefectInstancePropertiesResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link UpdateDefectInstanceProperties }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "updateDefectInstanceProperties")
    public JAXBElement<UpdateDefectInstanceProperties> createUpdateDefectInstanceProperties(UpdateDefectInstanceProperties value) {
        return new JAXBElement<UpdateDefectInstanceProperties>(_UpdateDefectInstanceProperties_QNAME, UpdateDefectInstanceProperties.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectsForStreamsResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectsForStreamsResponse")
    public JAXBElement<GetMergedDefectsForStreamsResponse> createGetMergedDefectsForStreamsResponse(GetMergedDefectsForStreamsResponse value) {
        return new JAXBElement<GetMergedDefectsForStreamsResponse>(_GetMergedDefectsForStreamsResponse_QNAME, GetMergedDefectsForStreamsResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link UpdateTriageForCIDsInTriageStore }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "updateTriageForCIDsInTriageStore")
    public JAXBElement<UpdateTriageForCIDsInTriageStore> createUpdateTriageForCIDsInTriageStore(UpdateTriageForCIDsInTriageStore value) {
        return new JAXBElement<UpdateTriageForCIDsInTriageStore>(_UpdateTriageForCIDsInTriageStore_QNAME, UpdateTriageForCIDsInTriageStore.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetFileContents }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getFileContents")
    public JAXBElement<GetFileContents> createGetFileContents(GetFileContents value) {
        return new JAXBElement<GetFileContents>(_GetFileContents_QNAME, GetFileContents.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link CovRemoteServiceException }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "CoverityFault")
    public JAXBElement<CovRemoteServiceException> createCoverityFault(CovRemoteServiceException value) {
        return new JAXBElement<CovRemoteServiceException>(_CoverityFault_QNAME, CovRemoteServiceException.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link CreateMergedDefectResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "createMergedDefectResponse")
    public JAXBElement<CreateMergedDefectResponse> createCreateMergedDefectResponse(CreateMergedDefectResponse value) {
        return new JAXBElement<CreateMergedDefectResponse>(_CreateMergedDefectResponse_QNAME, CreateMergedDefectResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectsForSnapshotScope }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectsForSnapshotScope")
    public JAXBElement<GetMergedDefectsForSnapshotScope> createGetMergedDefectsForSnapshotScope(GetMergedDefectsForSnapshotScope value) {
        return new JAXBElement<GetMergedDefectsForSnapshotScope>(_GetMergedDefectsForSnapshotScope_QNAME, GetMergedDefectsForSnapshotScope.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectHistoryResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectHistoryResponse")
    public JAXBElement<GetMergedDefectHistoryResponse> createGetMergedDefectHistoryResponse(GetMergedDefectHistoryResponse value) {
        return new JAXBElement<GetMergedDefectHistoryResponse>(_GetMergedDefectHistoryResponse_QNAME, GetMergedDefectHistoryResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link UpdateStreamDefects }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "updateStreamDefects")
    public JAXBElement<UpdateStreamDefects> createUpdateStreamDefects(UpdateStreamDefects value) {
        return new JAXBElement<UpdateStreamDefects>(_UpdateStreamDefects_QNAME, UpdateStreamDefects.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetCheckerSubcategoriesForProject }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getCheckerSubcategoriesForProject")
    public JAXBElement<GetCheckerSubcategoriesForProject> createGetCheckerSubcategoriesForProject(GetCheckerSubcategoriesForProject value) {
        return new JAXBElement<GetCheckerSubcategoriesForProject>(_GetCheckerSubcategoriesForProject_QNAME, GetCheckerSubcategoriesForProject.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetComponentMetricsForProjectResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getComponentMetricsForProjectResponse")
    public JAXBElement<GetComponentMetricsForProjectResponse> createGetComponentMetricsForProjectResponse(GetComponentMetricsForProjectResponse value) {
        return new JAXBElement<GetComponentMetricsForProjectResponse>(_GetComponentMetricsForProjectResponse_QNAME, GetComponentMetricsForProjectResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetTrendRecordsForProjectResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getTrendRecordsForProjectResponse")
    public JAXBElement<GetTrendRecordsForProjectResponse> createGetTrendRecordsForProjectResponse(GetTrendRecordsForProjectResponse value) {
        return new JAXBElement<GetTrendRecordsForProjectResponse>(_GetTrendRecordsForProjectResponse_QNAME, GetTrendRecordsForProjectResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetStreamDefects }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getStreamDefects")
    public JAXBElement<GetStreamDefects> createGetStreamDefects(GetStreamDefects value) {
        return new JAXBElement<GetStreamDefects>(_GetStreamDefects_QNAME, GetStreamDefects.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetStreamDefectsResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getStreamDefectsResponse")
    public JAXBElement<GetStreamDefectsResponse> createGetStreamDefectsResponse(GetStreamDefectsResponse value) {
        return new JAXBElement<GetStreamDefectsResponse>(_GetStreamDefectsResponse_QNAME, GetStreamDefectsResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link UpdateStreamDefectsResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "updateStreamDefectsResponse")
    public JAXBElement<UpdateStreamDefectsResponse> createUpdateStreamDefectsResponse(UpdateStreamDefectsResponse value) {
        return new JAXBElement<UpdateStreamDefectsResponse>(_UpdateStreamDefectsResponse_QNAME, UpdateStreamDefectsResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectsForProjectScope }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectsForProjectScope")
    public JAXBElement<GetMergedDefectsForProjectScope> createGetMergedDefectsForProjectScope(GetMergedDefectsForProjectScope value) {
        return new JAXBElement<GetMergedDefectsForProjectScope>(_GetMergedDefectsForProjectScope_QNAME, GetMergedDefectsForProjectScope.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectsForProjectScopeResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectsForProjectScopeResponse")
    public JAXBElement<GetMergedDefectsForProjectScopeResponse> createGetMergedDefectsForProjectScopeResponse(GetMergedDefectsForProjectScopeResponse value) {
        return new JAXBElement<GetMergedDefectsForProjectScopeResponse>(_GetMergedDefectsForProjectScopeResponse_QNAME, GetMergedDefectsForProjectScopeResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link UpdateTriageForCIDsInTriageStoreResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "updateTriageForCIDsInTriageStoreResponse")
    public JAXBElement<UpdateTriageForCIDsInTriageStoreResponse> createUpdateTriageForCIDsInTriageStoreResponse(UpdateTriageForCIDsInTriageStoreResponse value) {
        return new JAXBElement<UpdateTriageForCIDsInTriageStoreResponse>(_UpdateTriageForCIDsInTriageStoreResponse_QNAME, UpdateTriageForCIDsInTriageStoreResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetFileContentsResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getFileContentsResponse")
    public JAXBElement<GetFileContentsResponse> createGetFileContentsResponse(GetFileContentsResponse value) {
        return new JAXBElement<GetFileContentsResponse>(_GetFileContentsResponse_QNAME, GetFileContentsResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetTriageHistory }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getTriageHistory")
    public JAXBElement<GetTriageHistory> createGetTriageHistory(GetTriageHistory value) {
        return new JAXBElement<GetTriageHistory>(_GetTriageHistory_QNAME, GetTriageHistory.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectDetectionHistory }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectDetectionHistory")
    public JAXBElement<GetMergedDefectDetectionHistory> createGetMergedDefectDetectionHistory(GetMergedDefectDetectionHistory value) {
        return new JAXBElement<GetMergedDefectDetectionHistory>(_GetMergedDefectDetectionHistory_QNAME, GetMergedDefectDetectionHistory.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetTrendRecordsForProject }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getTrendRecordsForProject")
    public JAXBElement<GetTrendRecordsForProject> createGetTrendRecordsForProject(GetTrendRecordsForProject value) {
        return new JAXBElement<GetTrendRecordsForProject>(_GetTrendRecordsForProject_QNAME, GetTrendRecordsForProject.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectsForSnapshotScopeResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectsForSnapshotScopeResponse")
    public JAXBElement<GetMergedDefectsForSnapshotScopeResponse> createGetMergedDefectsForSnapshotScopeResponse(GetMergedDefectsForSnapshotScopeResponse value) {
        return new JAXBElement<GetMergedDefectsForSnapshotScopeResponse>(_GetMergedDefectsForSnapshotScopeResponse_QNAME, GetMergedDefectsForSnapshotScopeResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetTriageHistoryResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getTriageHistoryResponse")
    public JAXBElement<GetTriageHistoryResponse> createGetTriageHistoryResponse(GetTriageHistoryResponse value) {
        return new JAXBElement<GetTriageHistoryResponse>(_GetTriageHistoryResponse_QNAME, GetTriageHistoryResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectDetectionHistoryResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectDetectionHistoryResponse")
    public JAXBElement<GetMergedDefectDetectionHistoryResponse> createGetMergedDefectDetectionHistoryResponse(GetMergedDefectDetectionHistoryResponse value) {
        return new JAXBElement<GetMergedDefectDetectionHistoryResponse>(_GetMergedDefectDetectionHistoryResponse_QNAME, GetMergedDefectDetectionHistoryResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectsForStreams }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectsForStreams")
    public JAXBElement<GetMergedDefectsForStreams> createGetMergedDefectsForStreams(GetMergedDefectsForStreams value) {
        return new JAXBElement<GetMergedDefectsForStreams>(_GetMergedDefectsForStreams_QNAME, GetMergedDefectsForStreams.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link CreateMergedDefect }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "createMergedDefect")
    public JAXBElement<CreateMergedDefect> createCreateMergedDefect(CreateMergedDefect value) {
        return new JAXBElement<CreateMergedDefect>(_CreateMergedDefect_QNAME, CreateMergedDefect.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetMergedDefectHistory }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getMergedDefectHistory")
    public JAXBElement<GetMergedDefectHistory> createGetMergedDefectHistory(GetMergedDefectHistory value) {
        return new JAXBElement<GetMergedDefectHistory>(_GetMergedDefectHistory_QNAME, GetMergedDefectHistory.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link GetCheckerSubcategoriesForStreams }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://ws.coverity.com/v8", name = "getCheckerSubcategoriesForStreams")
    public JAXBElement<GetCheckerSubcategoriesForStreams> createGetCheckerSubcategoriesForStreams(GetCheckerSubcategoriesForStreams value) {
        return new JAXBElement<GetCheckerSubcategoriesForStreams>(_GetCheckerSubcategoriesForStreams_QNAME, GetCheckerSubcategoriesForStreams.class, null, value);
    }

}
