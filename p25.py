#!/usr/bin/env python

import scraperwiki
import requests
import urllib2
import lxml.etree

#URL lists and base URL at the bottom of scraper

#This strips out XML tags from the PDF so you are left with the text
def textonly(line):
    return line.split('>')[1].split('<')[0]

#Define a new function called 'scrapepdf' with 1 parameters: 'pdfurl' 
def scrapepdf(pdfurl, year):
    #use the .urlopen function from urllib library (imported at the start of this scraper) to open 
    #and the .read method to read into new variable 'pdfdata'
    try:
        pdfdata = urllib2.urlopen(pdfurl).read()
        #convert to an XML object so we can scrape using lxml.etree
        xmldata = scraperwiki.pdftoxml(pdfdata)
        #these lines throw up an error:
        #ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
        #root = lxml.etree.fromstring(xmldata)
        #Split to grab the pages with volunteer data. This needs to be put in separate function
        volunteerspage = xmldata.split('C1: Book Issues')[1]
        pagelines = volunteerspage.split('<text')
        #Because around a third of results don't get captured in that block, the next line just does the same for the whole doc
        doclines = xmldata.split('<text')
        indexline = -1
        perthou = 'CHECK THIS'
        aveperthou = 'CHECK THIS'
        issuesnum = 'CHECK THIS'
        #this is a counter which goes up for each match it finds (later in the if loop)
        #we hope this ends up 1 in the final spreadsheet to indicate only one thing at that position in the whole doc
        perthouNODUP = 0
        aveperthouNODUP = 0
        issuesnumNODUP = 0
        numberpos = 0
        for line in doclines:
            indexline = indexline+1
            if 'top="206"' in line and year==2012:
                print "FOUND", line
                if 'left="346"' in line:
                    perthou = line.split('>')[1].split('<')[0]
                    perthouNODUP = perthouNODUP+1
                    numberpos = 346
                if 'left="246"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 246
                    issuesnumNODUP = issuesnumNODUP+1
                if 'left="234"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 234
                    issuesnumNODUP = issuesnumNODUP+1
            elif 'top="209"' in line and year==2012:
                print "FOUND", line
                if 'left="346"' in line:
                    perthou = line.split('>')[1].split('<')[0]
                    perthouNODUP = perthouNODUP+1
                    numberpos = 346
                if 'left="246"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 246
                    issuesnumNODUP = issuesnumNODUP+1
                if 'left="234"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 234
                    issuesnumNODUP = issuesnumNODUP+1
            if '2,762,306' in line:
                print 'WHAT IS THE TOP POS?', line
                print 'WHAT IS THE LINE BEFORE?', doclines[indexline-1]
                print 'WHAT IS THE LINE AFTER?', doclines[indexline+1]
            if 'top="202"' in line and year==2014:
                print "FOUND", line
                if 'left="347"' in line:
                    perthou = line.split('>')[1].split('<')[0]
                    perthouNODUP = perthouNODUP+1
                if 'left="414"' in line:
                    aveperthou = line.split('i>')[1].split('<')[0]
                    aveperthouNODUP = aveperthouNODUP+1
                if 'left="250"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 250
                    issuesnumNODUP = issuesnumNODUP+1
                elif 'left="238"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 238
                    issuesnumNODUP = issuesnumNODUP+1
            if '894,378' in line:
                print 'WHAT IS THE TOP POS?', line
                print 'WHAT IS THE LINE BEFORE?', doclines[indexline-1]
                print 'WHAT IS THE LINE AFTER?', doclines[indexline+1]
        print "NUMBER OF LINES", len(pagelines)
        #print volunteerspage[:100000]
        linecount = -1
        bookissues = []
        for line in pagelines:
            if '2,488' in line:
                print 'WHAT IS THE TOP POS?', line
                print line.split('top="')[1].split('"')[0]
            if 'top="202"' in line:
                print "FOUND", line
                if 'left="347"' in line:
                    perthou = line.split('>')[1].split('<')[0]
                if 'left="414"' in line:
                    aveperthou = line.split('i>')[1].split('<')[0]
                if 'left="250"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 250
                elif 'left="238"' in line:
                    issuesnum = line.split('>')[1].split('<')[0]
                    numberpos = 238
                bookissues.append(line)
            linecount = linecount+1
        uniqueid = pdfurl+str(year)
        record['uniqueid'] = uniqueid
        record['yr'] = year
        record['perthou'] = perthou
        record['aveperthou'] = aveperthou
        record['issuesnum'] = issuesnum
        record['numberposition'] = numberpos
        record['pdfurl'] = pdfurl
        record['issuesnumNODUP'] = issuesnumNODUP
        record['perthouDUP'] = perthouNODUP
        record['aveperthouDUP'] = aveperthouNODUP
        print record
        scraperwiki.sql.save(['uniqueid'],record)
    except:
        print 'CANNOT SCRAPE', pdfurl
        errorlist.append(pdfurl)
    print 'errorlist', errorlist


record = {}
pdfurl = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/barking%20and%20dagenham.pdf'

#scrapepdf('http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202013/bournemouth.pdf')


#The PDFs themselves are at these URLs
for2012 = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/'
for201314 = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/'
#Each list of PDF names has been scraped using Outwit

pdflist12 = ['bath%20and%20north%20east%20somerset.pdf', 'barking%20and%20dagenham.pdf', 'barnet.pdf','barnsley.pdf','bexley.pdf','bedford.pdf','birmingham.pdf','bolton.pdf','bracknell%20forest.pdf','blackburn%20with%20darwen.pdf','blackpool.pdf','bournemouth.pdf','bromley.pdf','bury.pdf','buckinghamshire.pdf','brent.pdf','bristol.pdf','brighton%20and%20hove.pdf','cheshire%20east.pdf','calderdale.pdf','central%20bedfordshire.pdf','cambridgeshire.pdf','camden.pdf','cheshire%20west%20and%20chester.pdf','coventry.pdf','city%20of%20london.pdf','croydon.pdf','cumbria.pdf','cornwall.pdf','darlington.pdf','derby.pdf','derbyshire.pdf','doncaster.pdf','dorset.pdf','devon.pdf','dudley.pdf','durham.pdf','essex.pdf','gateshead.pdf','east%20sussex.pdf','enfield.pdf','ealing.pdf','greenwich.pdf','gloucestershire.pdf','hackney.pdf','halton.pdf','hammersmith%20and%20fulham.pdf','hampshire.pdf','hertfordshire.pdf','haringey.pdf','herefordshire.pdf','hartlepool.pdf','harrow.pdf','havering.pdf','hillingdon.pdf','kent.pdf','kensington%20and%20chelsea.pdf','hounslow.pdf','isle%20of%20wight.pdf','islington.pdf','kingstonuponhull.pdf','kingstonuponthames.pdf','lancashire.pdf','lambeth.pdf','kirklees.pdf','knowsley.pdf','leeds.pdf','lewisham.pdf','leicester.pdf','leicestershire.pdf','liverpool.pdf','lincolnshire.pdf','luton.pdf','merton.pdf','manchester.pdf','medway.pdf','middlesbrough.pdf','milton%20keynes.pdf','newcastle%20upon%20tyne.pdf','newham.pdf','norfolk.pdf','north%20east%20lincolnshire.pdf','north%20lincolnshire.pdf','north%20somerset.pdf','north%20tyneside.pdf','north%20yorkshire.pdf','oldham.pdf','northamptonshire.pdf','northumberland.pdf','nottinghamshire.pdf','nottingham.pdf','oxfordshire.pdf','peterborough.pdf','redbridge.pdf','portsmouth.pdf','poole.pdf','plymouth.pdf','reading.pdf','redcar%20%20cleveland.pdf','richmonduponthames.pdf','rochdale.pdf','rutland.pdf','salford.pdf','sandwell.pdf','rotherham.pdf','sefton.pdf','sheffield.pdf','solihull.pdf','somerset.pdf','shropshire.pdf','slough.pdf','south%20gloucestershire.pdf','south%20tyneside.pdf','stockport.pdf','staffordshire.pdf','southwark.pdf','st%20helens.pdf','southampton.pdf','southendonsea.pdf','stocktonontees.pdf','stokeontrent.pdf','suffolk.pdf','sunderland.pdf','surrey.pdf','sutton.pdf','swindon.pdf','tameside.pdf','telford%20and%20wrekin.pdf','thurrock.pdf','torbay.pdf','tower%20hamlets.pdf','trafford.pdf','wakefield.pdf','walsall.pdf','waltham%20forest.pdf','wandsworth.pdf','warrington.pdf','warwickshire.pdf','west%20berkshire.pdf','west%20sussex.pdf','westminster.pdf','wigan.pdf','wiltshire.pdf','windsor%20and%20maidenhead.pdf','wirral.pdf','wolverhampton.pdf','worcestershire.pdf','york.pdf']
pdflist14 = ['bexley.pdf','bath-and-north-east-somerset.pdf','barking-and-dagenham.pdf','barnet.pdf','bedford.pdf','barnsley.pdf','bournemouth.pdf','bracknell-forest.pdf','brent.pdf','blackpool.pdf','blackburn-with-darwen.pdf','brighton-and-hove.pdf','bolton.pdf','bristol.pdf','bromley.pdf','bury.pdf','buckinghamshire.pdf','cheshire-east.pdf','cambridgeshire.pdf','calderdale.pdf','central-bedfordshire.pdf','cheshire-west-and-chester.pdf','camden.pdf','cornwall.pdf','coventry.pdf','croydon.pdf','darlington.pdf','cumbria.pdf','derby.pdf','devon.pdf','derbyshire.pdf','doncaster.pdf','durham.pdf','ealing.pdf','dudley.pdf','east-sussex.pdf','dorset.pdf','essex.pdf','gateshead.pdf','enfield.pdf','gloucestershire.pdf','greenwich.pdf','hammersmith-and-fulham.pdf','hackney.pdf','halton.pdf','hampshire.pdf','harrow.pdf','hartlepool.pdf','herefordshire.pdf','hillingdon.pdf','havering.pdf','hertfordshire.pdf','isle-of-wight.pdf','hounslow.pdf','islington.pdf','kent.pdf','kingston-upon-hull.pdf','kensington-and-chelsea.pdf','lambeth.pdf','lancashire.pdf','kingston-upon-thames.pdf','lewisham.pdf','leicester.pdf','lincolnshire.pdf','leeds.pdf','luton.pdf','leicestershire.pdf','medway.pdf','newcastle-upon-tyne.pdf','milton-keynes.pdf','merton.pdf','newham.pdf','northamptonshire.pdf','north-lincolnshire.pdf','north-somerset.pdf','north-east-lincolnshire.pdf','north-tyneside.pdf','northumberland.pdf','manchester.pdf','nottingham.pdf','north-yorkshire.pdf','nottinghamshire.pdf','oldham.pdf','oxfordshire.pdf','poole.pdf','portsmouth.pdf','redbridge.pdf','peterborough.pdf','plymouth.pdf','reading.pdf','richmond-upon-thames.pdf','redcar-and-cleveland.pdf','rochdale.pdf','salford.pdf','sandwell.pdf','sefton.pdf','sheffield.pdf','shropshire.pdf','somerset.pdf','slough.pdf','solihull.pdf','southampton.pdf','south-tyneside.pdf','southend-on-sea.pdf','south-gloucestershire.pdf','southwark.pdf','staffordshire.pdf','st-helens.pdf','stoke-on-trent.pdf','stockton-on-tees.pdf','stockport.pdf','sunderland.pdf','sutton.pdf','suffolk.pdf','surrey.pdf','swindon.pdf','torbay.pdf','tameside.pdf','tower-hamlets.pdf','telford-and-wrekin.pdf','thurrock.pdf','wandsworth.pdf','warrington.pdf','wakefield.pdf','walsall.pdf','waltham-forest.pdf','trafford.pdf','west-berkshire.pdf','westminster.pdf','warwickshire.pdf','wigan.pdf','west-sussex.pdf','wolverhampton.pdf','wiltshire.pdf','wirral.pdf','windsor-and-maidenhead.pdf','worcestershire.pdf','york.pdf']

testlist = ['http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/city%20of%20london.pdf','http://www.cipfa.org/~/media/files/services/research and statistics/cipfastats library profiles/bath and north east somerset', 'http://www.cipfa.org/~/media/files/services/research and statistics/cipfastats library profiles/bedford']
testlist14 = [ 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/barnsley.pdf']
testbexley = ['http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/cheshire-east.pdf']

errorlist = []
pdflisttest = ['buckinghamshire.pdf']

#Testing this group against the same TOP/LEFT positions
# URL 404 error - but works when put in browser
for item in pdflist12:
    print 'SCRAPING', for2012+item
    scrapepdf(for2012+item, 2012)

#This loop works
'''
for item in pdflist14:
    print 'SCRAPING', for201314+item
    scrapepdf(for201314+item, 2014)

'''
