#!/usr/local/bin/python

import sys, os, pystache, urllib, pprint

'''
WordPress localizations are pretty weird.
Some only consist of a language code (like 'fi'). 
Some have a language and country code (like de-DE). 
en-US as default langugage is not encoded at all and falls back to an empty string.

Table:
Languages covered by the available WP localizations without country codes and their corresponding country codes.
Coutries for the arab language taken from http://en.wikipedia.org/wiki/Arabic_language#mediaviewer/File:Arabic_speaking_world.svg

langcode	Country
	'ar'	'eg','dz','bh','dj','er','iq','il','ye','jo','qa','km','kw','lb','ly','ma','mr','om','sa','so','sd','sy','td','tn','ae',
	'az'	'az',
	'ca'	'fr',
	'cy'	'gb',
	'eu'	'es',
	'fi'	'fi',
	'gd'	'gb',
	'hr'	'hr',
	'ja'	'jp',
	'th'	'th',

Languages known for beiong spoken in than one country
(there are likely more, will researching this later)
	Language	Country codes
	'de'		'ch','at','be'
	'es'		'es','gq','cr','do','sv','gt','hn','cu','mx','ni','pa','pr','ar','bo','cl','ec','co','py','pe','uy','ve'
	'pt'		'pt','ao','br','gq','gw','cv','mz','st','mo','tl'
	'fr'		'fr','ca',
'''

# country codes covered by WordPress
wp_codes = ['bg','ba','dk','de','ca','gb','au','es','pe','cl','ir','fr','es','il','hu','id','it','kr','mm','no','nl','pl','pt','br','ru','sk','rs','se','tr','cn','tw','us']

	

do_codes = []

css_template = """


.i18n-item[data-country][lang],
.i18n-item[data-country][data-language] {
	position:relative;
}

.i18n-item[lang]:after,
.i18n-item[data-language]:after,
.i18n-item[data-country]:before {
	content:' ';
	display: inline-block;
	width: 1.3333333333333333em;
	height:1em;
	background-size: 1.3333333333333333em 1em;
	background-position: center center;
	background-repeat: no-repeat;
}
.i18n-item[data-country][data-language]:before,
.i18n-item[data-country][lang]:before {
	margin-right:0.5em;
}
.i18n-item[lang]:after,
.i18n-item[data-language]:after {
	text-align:center;
	text-transform:uppercase;
	font-size: 0.8em;
	line-height:1.0em;
	font-weight:bold;
	color:#000;
	background-color:transparent;
	border:1px solid rgba(30,30,30,0.8);
	background-color:rgba(255,255,255,0.9);
	width: 1.3333333333333333em;
	height:1em;
	padding:0.0125em 0.125em;
	box-sizing:content-box;
}
.i18n-item.invert:after {
	color:#fff;
	border-style:none;
	background-color:rgba(0,0,0,0.65);
}
.i18n-item[data-country][lang]:after,
.i18n-item[data-country][data-language]:after {
	position:absolute;
	left:1.1em;
	top:0.8em;
	font-size:0.6em;
	width: auto;
	height:auto;
}
.i18n-item[lang]:after {
	float:left;
}
.i18n-item[data-country][lang]:after {
	float:none;
}

.i18n-item[lang]:after {
	content:attr(lang);
}
.i18n-item[data-language]:after {
	content:attr(data-language);
}


{{#country_codes}}
.i18n-item[data-country='{{country_code_lower}}']:before,
.i18n-item[data-country='{{country_code_upper}}']:before {
	background-image:url( '../flags/4x3/{{country_code_lower}}.svg' );
}
{{/country_codes}}
"""
#	background-image:url( 'data:image/svg+xml;base64,{{flag_data}}' );


flag_path = os.path.dirname(os.path.realpath(__file__))+'/flags/4x3/'
out_path = os.path.dirname(os.path.realpath(__file__))+'/css/l18n.css'
template_data = {
	'country_codes':[]
}

for entry in os.listdir(flag_path):
	entry_path = os.path.join(flag_path,entry)
	country_code = os.path.splitext(entry)[0]
	if not len(do_codes) or country_code in do_codes:
		svg_code = open(entry_path,'rb').read()
		template_data['country_codes'].append({
			'country_code_lower':country_code.lower(),
			'country_code_upper':country_code.upper(),
			'flag_data':urllib.quote( svg_code.encode('base64') )
		})

content = pystache.render( css_template, template_data)
f = open(out_path,'w')
f.write(content)
f.close()

#print repr(template_data)
	
