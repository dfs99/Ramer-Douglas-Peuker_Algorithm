RAMER DOUGLAS PEUKER ALGORITHM
==============================================================================
  Requirements:

    In order to use successfully the Ramer Douglas Peuker Algorithm, you must
    need to install python3. If any problem arise while executing gif generator
    check Problems section.

  OPTIONS:

    RamerDouglasPeukerAlgorithm [-h]
      -h: Shows the helper text.

    RamerDouglasPeukerAlgorithm [-i]
      -i: Initialises the project creating a venv and installing all requirements
          from requirements.txt; Activates the venv and copies the src code into
          lib/site-packages in order to use the modules.

    RamerDouglasPeukerAlgorithm [-r]
      -r: Removes the virtual environment used to run the project.

    RamerDouglasPeukerAlgorithm [-b file error]
      -b file error: Generates a gif using the file argument, which must
                     be a bmp file (.bmp), and the given epsilon error used
                     in the algorithm.

    RamerDouglasPeukerAlgorithm [-f file error]
      -f file error: Generates a text file that contains the set of points
                     obtained in the algorithm. Uses a bmp file (.bmp) and
                     a given epsilon error.

    RamerDouglasPeukerAlgorithm [-t file]
      -t file: Generates a gif using the file argument. The file must be a
               .txt file and must contain the epsilon error, the total number
               of points and all the points to be used.

    RamerDouglasPeukerAlgorithm [-x file]
      -x file: Generates a text file that contains the set of points obtained
               in the algorithm. Uses a text file that must contain the epsilon
               error, the total number of points and all the points.


  FILES:

    bmp file: required @ -b and -f options. The bmp file must be 24bpp (bits
              per pixel) in order to work.

    text file: required @ -t and -x options. It must contain the data as
               follows:
                  1-.) the fist line must contain the epsilon error in order
                       to perform the algorithm.
                  2-.) the second line must contain the total number of points
                       within the file.
                  3-.) A point will be represented in two-dimensional plane
                       where x coordinate will be in first place. Afterwards,
                       the y coordinate should follow the x one separated by a
                       blank space. An example could be:
                          1 2.6
                          5 2
                          100.3 43
                  4-.) Repeated points will be ignored by default within the
                       algorithm.


  PROBLEMS:

    The main problem you may face is parallel lines in both images and text
    files. If the two lines used to get the distance are parallel, they will
    never cut each other.
    
    Another problem may arise when generating gif is not to have a GUI backend.
    The solution I've found is to install tkinter. 
        sudo apt-get install python3-tk



