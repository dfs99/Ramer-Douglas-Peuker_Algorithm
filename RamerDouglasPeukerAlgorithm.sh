#!/bin/bash
HELP_TEXT="
******************************************************************************
==============================================================================
                      RAMER DOUGLAS PEUKER ALGORITHM
==============================================================================
******************************************************************************


==============================================================================
  => Requirements:
==============================================================================
    In order to use successfully the Ramer Douglas Peuker Algorithm, you must
    need to install python3 and
    #TODO CORREGIR PROBLEMAS MATPLOT LIB EN LINUX.

==============================================================================
  => OPTIONS:
==============================================================================
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

==============================================================================
  => FILES:
==============================================================================
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

==============================================================================
  => PROBLEMS:
==============================================================================
    The main problem you may face is parallel lines in both images and text
    files. If the two lines used to get the distance are parallel, they will
    never cut each other.

******************************************************************************
"
USAGE_TEXT="Usage: RamerDouglasPeukerAlgorithm [-h] [-i] [-r] [-b file error] [-f file error] [-t file] [-x file]"
NO_ARGS_TEXT="Error: No args introduced: \n"

PYTHON=venv/bin/python3
PYTHON_FILE=src/RamerDouglasPeuker_algorithm.py

if [ $# -eq 0 ]; then
  echo -e "$NO_ARGS_TEXT" "$USAGE_TEXT"
  exit 1
else
  while getopts ":irhb:f:t:x" opt; do
    case $opt in
        i )
            python3 -m venv venv
            cd venv/
            source bin/activate
            cd ..
            pip install -r requirements.txt
            cp -R src venv/lib/python3.8/site-packages
            exit 0;;
        r )
            rm -r venv/
            exit 0;;
        h ) echo "$HELP_TEXT"
            exit 0;;
        b )
            shift
            $PYTHON $PYTHON_FILE b $1 $2
            # delete intermediary files.
            rm -r rdp*.txt
          ;;
        f )
            shift
            $PYTHON $PYTHON_FILE f $1 $2
          ;;
        t )
            shift
            $PYTHON $PYTHON_FILE t $1
          ;;
        x )
            shift
            $PYTHON $PYTHON_FILE x $1
          ;;
        ? ) echo -e "ERROR:\n $USAGE_TEXT"
             exit 1;;
     esac
done
fi
exit 0
