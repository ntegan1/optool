#!/usr/bin/env python3

def head():
  return """
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script src="https://cdn.tailwindcss.com"></script>
      <script src="https://xenova.github.io/draggable/dist/draggable.min.js"></script>
      <script>
        tailwind.config = {
          theme: {
            extend: {
              width: {
              '1/8': '12.5%',
              },
              height: {
              '1/8': '12.5%',
              },
              colors: {
                clifford: '#da373d',
                'invalidred': {
                  DEFAULT: '#FF6B75',
                },
	  		  'nord0': '#2E3440',
	  		  'nord1': '#3B4252',
	  		  'nord2': '#434C5E',
	  		  'nord3': '#4C566A',
	  		  'nord4': '#D8DEE9',
	  		  'nord5': '#E5E9F0',
	  		  'nord6': '#ECEFF4',
	  		  'nord7': '#8FBCBB',
	  		  'nord8': '#88C0D0',
	  		  'nord9': '#81A1C1',
	  		  'nord10': '#5E81AC',
	  		  'nord11': '#BF616A',
	  		  'nord12': '#D08770',
	  		  'nord13': '#EBCB8B',
	  		  'nord14': '#A3BE8C',
	  		  'nord15': '#B48EAD',
              }
            }
          }
        }
      </script>
    </head>
    """
