SUB = {
    'adsh' : ['Accession Number',str],
    'cik' : ['Central Index Key',int],
    'name' : ['Name of Registrant',str],
    'sic' : ['Standard Industrial Classification',int],
    'countryba' : ['Country of Buisiness Address',str],
    'stprba' : ['City of Buisiness Address',str],
    'zipba' :  ['Zip code of Buisiness Address',str],
    'bas1' : ['First line of Address',str],
    'bas2' : ['Second line of Address',str],
    'baph' : ['Buisiness Address Phone Number',str],
    'cityma' : ['City of Mailing Address',str],
    'zipma' : ['Zip code of Mailing Address',str],
    'mas1' : ['First line of Mailing Address', str],
    'mas2' : ['Second line of Mailing Address', str],
    'countryinc' : ['Country of Incorporation', str],
    'stpinc' : ['State or Province of Registrant (US/CAN)',str],
    'ein' : ['Employee Identification Number', int],
    'former' : ['Most Recent Former Name', str],
    'changed' : ['Date of Name Change', str],
    'afs' : ['Filer Status (Filer_Dict)',str],
    'wksi' : ['Well Known Seasoned Issuer',bool],
    'fye' : ['Fiscal Year End Date', str],
    'form' : ['Submission Type',str],
    'period' : ['Balance Sheet Date', 'YYMMDD: DATE'],
    'fy' : ['Fiscal Year Focus', 'YYYY: Year'],
    'fp' : ['Fiscal Period Focus', str],
    'filed' : ['Date of Filing', 'YYMMDD: DATE'],
    'accepted' : ['Date of Filing Acceptance', str],
    'prevrpt' : ['Amended Version Available', bool],
    'detail' : ['Quantitative Info in Footnotes',bool],
    'instance' : ['Name of Original XBRL File',str],
    'nciks' : ['Number of Central Index Keys included',int],
    'aciks' : ['Additional CIKs', str]
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
    'abstract' : ['Non-Numeric Fact',bool],
    'datatype' : ['Datatype (if Numeric)',bool],
    'iord' : ['I=Point In Time, D=Duration',str],
    'crdr' : ['Debit or Credit', 'C or D'],
    'tlabel' : ['Label Text',str],
    'doc' : ['Detailed Definition', str]
}

NUM = {
    'adsh' : ['Accession Number',str],
    'tag' : ['Unique Name for Taxonomy Release', str],
    'version' : ['Identifier of Taxonomy/Accession Number',str],
    'coreg' : ['Indicates Co-Registrant (eg. Parent Company)',int],
    'ddate' : ['Date Value End Date', str],
    'qtrs' : ['Quarters Represented by Data', int],
    'uom' : ['Unit of Measure', str],
    'value' : ['Value', float],
    'footnote' : ['Footnotes', str]
}

PRE = {
    'adsh' : ['Accession Number',str],
    'report' : ['Type of Statement?', int],
    'line' : ['Line Order', int],
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