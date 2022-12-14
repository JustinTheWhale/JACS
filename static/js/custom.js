if($.browser.mozilla||$.browser.opera ){document.removeEventListener("DOMContentLoaded",jQuery.ready,false);document.addEventListener("DOMContentLoaded",function(){jQuery.ready()},false)}
jQuery.event.remove( window, "load", jQuery.ready );
jQuery.event.add( window, "load", function(){jQuery.ready();} );
jQuery.extend({
	includeStates:{},
	include:function(url,callback,dependency){
		if ( typeof callback!='function'&&!dependency){
			dependency = callback;
			callback = null;
		}
		url = url.replace('\n', '');
		jQuery.includeStates[url] = false;
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.onload = function () {
			jQuery.includeStates[url] = true;
			if ( callback )
				callback.call(script);
		};
		script.onreadystatechange = function () {
			if ( this.readyState != "complete" && this.readyState != "loaded" ) return;
			jQuery.includeStates[url] = true;
			if ( callback )
				callback.call(script);
		};
		script.src = url;
		if ( dependency ) {
			if ( dependency.constructor != Array )
				dependency = [dependency];
			setTimeout(function(){
				var valid = true;
				$.each(dependency, function(k, v){
					if (! v() ) {
						valid = false;
						return false;
					}
				})
				if ( valid )
					document.getElementsByTagName('body')[0].appendChild(script);
				else
					setTimeout(arguments.callee, 10);
			}, 10);
		}
		else
			document.getElementsByTagName('body')[0].appendChild(script);
		return function(){
			return jQuery.includeStates[url];
		}
	},

	readyOld: jQuery.ready,
	ready: function () {
		if (jQuery.isReady) return;
		imReady = true;
		$.each(jQuery.includeStates, function(url, state) {
			if (! state)
				return imReady = false;
		});
		if (imReady) {
			jQuery.readyOld.apply(jQuery, arguments);
		} else {
			setTimeout(arguments.callee, 10);
		}
	}
});

/* ---------------------------------------------------------------------- */
/*	Include Javascript Files
/* ---------------------------------------------------------------------- */

	$.include('js/jquery.easing.1.3.js');
	$.include('js/jquery.cycle.all.min.js');
	$.include('js/respond.min.js');
	
	if(jQuery('.video-image').length) {
		$.include('fancybox/jquery.fancybox.pack.js');
	}
	
	//	Panel
	$.include('changer/js/changer.js');
	$.include('changer/js/colorpicker.js');
	
/* end  */

/************************************************************************/
/* DOM READY --> Begin													*/
/************************************************************************/

jQuery(document).ready(function($) {
	
	/* ---------------------------------------------------- */
	/*	Main Navigation
	/* ---------------------------------------------------- */

	(function() {

		var	arrowimages = {
			down: 'downarrowclass',
			right: 'rightarrowclass'
		};
		var $mainNav    = $('#navigation').find('> ul'),
			optionsList = '<option value="" selected>Navigation</option>';

			var $submenu = $mainNav.find("ul").parent();
			$submenu.each(function (i) {
				var $curobj = $(this);
					this.istopheader = $curobj.parents("ul").length == 1 ? true : false;
				$curobj.children("a").append('<span class="' + (this.istopheader ? arrowimages.down : arrowimages.right) +'"></span>');
			});
		
		$mainNav.on('mouseenter', 'li', function() {
			var $this    = $(this),
				$subMenu = $this.children('ul');
			if($subMenu.length) $this.addClass('hover');
			$subMenu.hide().stop(true, true).fadeIn(200);
		}).on('mouseleave', 'li', function() {
			$(this).removeClass('hover').children('ul').stop(true, true).fadeOut(50);
		});

		// Navigation Responsive

		$mainNav.find('li').each(function() {
			var $this   = $(this),
				$anchor = $this.children('a'),
				depth   = $this.parents('ul').length - 1,
				dash  = '';

			if(depth) {
				while(depth > 0) {
					dash += '--';
					depth--;
				}
			}

			optionsList += '<option value="' + $anchor.attr('href') + '">' + dash + ' ' + $anchor.text() + '</option>';

		}).end()
			.after('<select class="nav-responsive">' + optionsList + '</select>');

		$('.nav-responsive').on('change', function() {
			window.location = $(this).val();
		});

	})();

	/* end Main Navigation */
	
	/* ---------------------------------------------------- */
	/*	Cookie
	/* ---------------------------------------------------- */

	jQuery.cookie = function (name, value, options) {
		if (typeof value != 'undefined') {
			options = options || {};
			if (value === null) {
				value = '';
				options.expires = -1
			}
			var expires = '';
			if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
				var date;
				if (typeof options.expires == 'number') {
					date = new Date();
					date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000))
				} else {
					date = options.expires
				}
				expires = '; expires=' + date.toUTCString()
			}
			var path = options.path ? '; path=' + (options.path) : '';
			var domain = options.domain ? '; domain=' + (options.domain) : '';
			var secure = options.secure ? '; secure' : '';
			document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('')
		} else {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break
					}
				}
			}
			return cookieValue
		}
	};
	
	/* end Cookie */
	
	/* ---------------------------------------------------- */
	/*	Loan Calculator
	/* ---------------------------------------------------- */
	
	var LOAN_CALCULATOR_OBJECT = function(){

		var self = {
			form: $('#loan'),
			calculate: function() {
				var DownPayment= "0";
				self.get_amount();
				self.get_annual_rate();
				self.get_years();

				var MonthRate = AnnualRate / 12;
				var NumPayments = Years * 12;
				var Prin = LoanAmount - DownPayment;
				var MonthPayment = Math.floor((Prin*MonthRate)/(1-Math.pow((1+MonthRate),(-1*NumPayments)))*100)/100;

				self.update_number_payments(NumPayments);
				self.update_monthly_payment(MonthPayment);
			},
			init: function() {
				self.calculate();
				$("[name=cal]", self.form).on("click",function(e){
					self.calculate();
					e.preventDefault();
				})
			},
			get_amount: function(){
				return LoanAmount = $('[name=LoanAmount]', self.form).val();
			},
			get_annual_rate: function() {
				return AnnualRate = $('[name=InterestRate]', self.form).val()/100;
			},
			get_years: function() {
				return Years = $('[name=NumberOfYears]', self.form).val();
			},
			update_number_payments: function(NumPayments) {
				return self.form.find('[name=NumberOfPayments]').val(NumPayments);
			},
			update_monthly_payment: function(MonthPayment) {
				return self.form.find('[name=MonthlyPayment]').val(MonthPayment);		
			}
		}

		return self;

	}

	var LOAN = new LOAN_CALCULATOR_OBJECT();
	LOAN.init();

	/* end Loan Calculator */		

	/* ---------------------------------------------------- */
	/*	Fit Videos
	/* ---------------------------------------------------- */

	(function() {

		$('.container').each(function(){
			var target  = [
				"iframe[src^='http://www.youtube.com']",
				"iframe[src^='http://player.vimeo.com']",
				"object"
			];

				$allVideos = $(this).find(target.join(','));

			$allVideos.each(function(){
				var $this = $(this);

				if (this.tagName.toLowerCase() == 'embed' && $this.parent('object').length || $this.parent('.liquid-video-wrapper').length) {return;} 
				var height = this.tagName.toLowerCase() == 'object' ? $this.attr('height') : $this.height(),
				aspectRatio = height / $this.width();

				if(!$this.attr('id')){
					var $ID = Math.floor(Math.random()*9999999);
					$this.attr('id', $ID);
				}
				$this.wrap('<div class="liquid-video-wrapper"></div>').parent('.liquid-video-wrapper').css('padding-top', (aspectRatio * 100)+"%");
				$this.removeAttr('height').removeAttr('width');
			});
		});
		
	})();

	/* end Fit Videos */
	
	/* ---------------------------------------------------- */
	/*	Galleriffic
	/* ---------------------------------------------------- */
	
	if($('#thumbs').length){
		
		var gallery = $('#thumbs').galleriffic({
			delay:                     2500,
			numThumbs:                 15,
			preloadAhead:              10,
			enableTopPager:            true,
			enableBottomPager:         true,
			maxPagesToShow:            7,
			imageContainerSel:         '#slideshow',
			controlsContainerSel:      '#controls',
			captionContainerSel:       '#caption',
			loadingContainerSel:       '#loading',
			renderSSControls:          true,
			renderNavControls:         true,
			playLinkText:              'Play Slideshow',
			pauseLinkText:             'Pause Slideshow',
			prevLinkText:              '&lsaquo; Previous Photo',
			nextLinkText:              'Next Photo &rsaquo;',
			nextPageLinkText:          'Next &rsaquo;',
			prevPageLinkText:          '&lsaquo; Prev',
			enableHistory:             false,
			autoStart:                 false,
			syncTransitions:           true,
			defaultTransitionDuration: 900,
			onPageTransitionOut:       function(callback) {
				this.fadeTo('fast', 0.0, callback);
			},
			onPageTransitionIn:        function() {
				this.fadeTo('fast', 1.0);
			}
		});
		
	}

	/* end Galleriffic */		

	/* ---------------------------------------------------- */
	/*	jQuery Cookie
	/* ---------------------------------------------------- */

	jQuery.cookie = function (name, value, options) {
		if (typeof value != 'undefined') {
			options = options || {};
			if (value === null) {
				value = '';
				options.expires = -1
			}
			var expires = '';
			if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
				var date;
				if (typeof options.expires == 'number') {
					date = new Date();
					date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000))
				} else {
					date = options.expires
				}
				expires = '; expires=' + date.toUTCString()
			}
			var path = options.path ? '; path=' + (options.path) : '';
			var domain = options.domain ? '; domain=' + (options.domain) : '';
			var secure = options.secure ? '; secure' : '';
			document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('')
		} else {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break
					}
				}
			}
			return cookieValue
		}
	};
	
	/* end jQuery Cookie */
	
	/* ---------------------------------------------------- */
	/*	Min. Height
	/* ---------------------------------------------------- */

	(function() {

		$('section.container').not('#footer section.container')
		.css( 'min-height', $(window).outerHeight(true) 
			- $('#header').outerHeight(true) 
			- $('#footer').outerHeight(true));

	})();

	/* end Min. Height */
	
	
	/* ---------------------------------------------------- */
	/*	Widget Title
	/* ---------------------------------------------------- */
	
	(function() {

		var activeTitle = $('.widget-title, .section-title');

		activeTitle.each(function(){
			var titleItem = $(this).text();
			var text = titleItem.split(" ");
			var first = text.shift();
			$(this).html("<span>" + first + " " + "</span>" + text.join(" "));
		});			

	})();
		
	/* end Widget Title */
	
	/* ---------------------------------------------------------------------- */
	/*	Toggle
	/* ---------------------------------------------------------------------- */

	(function() {
		
		if($('.toggle-container').length) {

			var container = $('.toggle-container'),
				trigger   = $('.trigger');

			container.hide();
			trigger.first().addClass('active').next().show();

			trigger.on('click', function(e) {
				if($(this).next().is(':hidden') ) {
					trigger.removeClass('active').next().slideUp(300);
					$(this).toggleClass('active').next().slideDown(300);
				}
				e.preventDefault();
			});	
		}

	})();

	/* end Toggle */

	/* ---------------------------------------------------- */
	/*	Entry Tabs
	/* ---------------------------------------------------- */

	(function() {

		if($('.entry-tabs').length) {

			var $contentTabs  = $('.entry-tabs');

			$.fn.tabs = function($obj) {
					$tabsNavLis = $obj.find('.tabs-nav').children('li'),
					$tabContent = $obj.find('.tab-content');

				$tabContent.hide();	
				$tabsNavLis.first().addClass('active').show();
				$tabContent.first().show();

				$obj.find('ul.tabs-nav li').on('click', function(e) {
					var $this = $(this);

						$obj.find('ul.tabs-nav li').removeClass('active');
						$this.addClass('active');
						$obj.find('.tab-content').hide(); //Hide all tab content
						$($this.find('a').attr('href')).fadeIn();

					e.preventDefault();
				});
			}

			$contentTabs.tabs($contentTabs);
		}

	})();

	/* end Content Tabs */

	/* ---------------------------------------------------- */
	/*	Listing Tabs
	/* ---------------------------------------------------- */
	/*
	(function() {
		
		var switcher = $('.layout-switcher'),
			item = $('#change-items');

		if(switcher.length) {
			
			$.fn.tabsEntry = function($obj) {
				
			var nav = $.cookie('nav');
			var href = $.cookie('href');
			
					var	$tabsNavLis = $obj.find('a');
						
				if (nav && href) {
					$tabsNavLis.removeClass("active");
					$tabsNavLis.filter('.' + nav).addClass('active');
					item.removeClass().addClass(href);
				}	else {
					$tabsNavLis.removeClass("active");
					$tabsNavLis.first().addClass('active');
				}	
				
				$tabsNavLis.on('click', function(e) {
					
					var $this = $(this);
					
							nav = $(this).attr("class"),
							href = $(this).attr("href").substring(1);
							
							$.cookie("nav", nav);
							$.cookie("href", href);
							item.removeClass().addClass(href);
						
						$tabsNavLis.removeClass('active');
						$this.addClass('active');

					e.preventDefault();
				});
			}
			
			switcher.tabsEntry(switcher);
		}

	})();
	*/
	/* end Listing Tabs */

	/* ---------------------------------------------------- */
	/*	Back to Top
	/* ---------------------------------------------------- */

	(function() {

		var extend = {
				button      : '#back-top',
				text        : 'Back to Top',
				min         : 200,
				fadeIn      : 400,
				fadeOut     : 400,
				speed		: 800,
				easing		: 'easeOutQuint'
			},
			oldiOS     = false,
			oldAndroid = false;
			
		// Detect if older iOS device, which doesn't support fixed position
		if( /(iPhone|iPod|iPad)\sOS\s[0-4][_\d]+/i.test(navigator.userAgent) )
			oldiOS = true;

		// Detect if older Android device, which doesn't support fixed position
		if( /Android\s+([0-2][\.\d]+)/i.test(navigator.userAgent) )
			oldAndroid = true;

		$('body').append('<a href="#" id="' + extend.button.substring(1) + '" title="' + extend.text + '">' + extend.text + '</a>');

		$(window).scroll(function() {
			var pos = $(window).scrollTop();
			
			if( oldiOS || oldAndroid ) {
				$( extend.button ).css({
					'position' : 'absolute',
					'top'      : position + $(window).height()
				});
			}
			
			if (pos > extend.min) {
				$(extend.button).fadeIn(extend.fadeIn);
			}
				
			else {
				$(extend.button).fadeOut (extend.fadeOut);
			}
				
		});

		$(extend.button).click(function(e){
			$('html, body').animate({scrollTop : 0}, extend.speed, extend.easing);
			e.preventDefault();
		});

	})();

	/* end Back to Top */
				
/************************************************************************/
});/* DOM READY --> End													*/
/************************************************************************/
