
if False:
	print('可去运行XJ.Widgets.XJQ_PictCarousel._test以查看效果')
	file='Pict.webp'
	# file='Movie.mp4'
	gm=XJ_GIFMaker()
	print("LOAD")
	gm.Opt_LoadSource(file)
	print("TRANS")
	gm.Opt_SaveGif('Trans.gif',callback=lambda data:print("FINISH"))



