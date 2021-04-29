SUB = {
    'adsh' : ['Accession Number',str],
    'cik' : ['Central Index Key',float],
    'name' : ['Name of Registrant',str],
    'sic' : ['Standard Industrial Classification',float],
    'countryba' : ['Country of Buisiness Address',str],
    'stprba' : ['City of Buisiness Address',str],
    'zipba' :  ['Zip code of Buisiness Address',str],
    'bas1' : ['First line of Address',str],
    'bas2' : ['Second line of Address',str],
    'baph' : ['Buisiness Address Phone Number',str],
    'countryma' : ['Registrants Mailing Address', str],
    'stprma' : ['Mailing Address', str],
    'cityma' : ['City of Mailing Address',str],
    'zipma' : ['Zip code of Mailing Address',str],
    'mas1' : ['First line of Mailing Address', str],
    'mas2' : ['Second line of Mailing Address', str],
    'countryinc' : ['Country of Incorporation', str],
    'stpinc' : ['State or Province of Registrant (US/CAN)',str],
    'ein' : ['Employee Identification Number', float],
    'former' : ['Most Recent Former Name', str],
    'changed' : ['Date of Name Change', str],
    'afs' : ['Filer Status (Filer_Dict)',str],
    'wksi' : ['Well Known Seasoned Issuer',bool],
    'fye' : ['Fiscal Year End Date', str],
    'form' : ['Submission Type',str],
    'period' : ['Balance Sheet Date', float],
    'fy' : ['Fiscal Year Focus', float],
    'fp' : ['Fiscal Period Focus', str],
    'filed' : ['Date of Filing', float],
    'accepted' : ['Date of Filing Acceptance', str],
    'prevrpt' : ['Amended Version Available', bool],
    'detail' : ['Quantitative Info in Footnotes',bool],
    'instance' : ['Name of Original XBRL File',str],
    'nciks' : ['Number of Central Index Keys included',float],
    'aciks' : ['Additional CIKs', str],
    'pubfloatusd' : ['Public Float USD', float],
    'floatdate' : ['Public Float measured by filer', float],
    'floataxis' : ['Computed by summing tagged values', str],
    'floatmems' : ['Number of terms in summation', float]
}

FILER_DICT = {
    'LAF' : 'Large Accelerated',
    'ACC' : 'Accelerated',
    'SRA' : 'Smaller Reporting, Accelerated',
    'NON' : 'Non-Accelerated',
    'SML' : 'Smaller Reporting Filer',
    'NULL' : 'Not Assigned'
}

TAG = {
    'tag' : ['Unique Name for Taxonomy Release', str],
    'version' : ['Identifier of Taxonomy/Accession Number',str],
    'custom' : ['Custom Tag', bool],
    'abstract' : ['Non-Numeric Fact', bool],
    'datatype' : ['Datatype (if Numeric)', str],
    'iord' : ['I=Point In Time, D=Duration', str],
    'crdr' : ['Debit or Credit', str],
    'tlabel' : ['Label Text',str],
    'doc' : ['Detailed Definition', str]
}

NUM = {
    'adsh' : ['Accession Number',str],
    'tag' : ['Unique Name for Taxonomy Release', str],
    'version' : ['Identifier of Taxonomy/Accession Number',str],
    'coreg' : ['Indicates Co-Registrant (eg. Parent Company)',str],
    'ddate' : ['Date Value End Date', float],
    'qtrs' : ['Quarters Represented by Data', float],
    'uom' : ['Unit of Measure', str],
    'value' : ['Value', float],
    'footnote' : ['Footnotes', str]
}

PRE = {
    'adsh' : ['Accession Number',str],
    'report' : ['Type of Statement?', float],
    'line' : ['Line Order', float],
    'stmt' : ['Financial Statement', str],
    'inpth' : ['Presented Parenthetically', bool],
    'rfile' : ['Type of Interactive Data File', str],
    'tag' : ['Tag Chosen by Filer', str],
    'version' : ['Taxonomy Identifier/adsh', str],
    'plabel' : ['Text Presented on Line Item (Preferred Label)', str]
}

DIM = {
    'dimh' : ['Hexadecimal', str],
    'segments' : ['Alphanumeric', str],
    'segt' : ['Boolean', bool]
}

KEYS = ['adsh','report','line','uom','qtrs','coreg','ddate','version','tag']