import mdtex2html
res = mdtex2html.convert(r'$$ \sigma = \sqrt{ \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2 } $$')
with open('test.html', 'w') as f:
	f.write(res)
