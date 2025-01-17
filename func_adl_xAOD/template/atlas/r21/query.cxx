#include <AsgTools/MessageCheck.h>
#include <analysis/query.h>
#include "xAODRootAccess/tools/TFileAccessTracer.h"

{% for i in body_include_files %}
#include "{{i}}"
{% endfor %}

#include <TTree.h>

query :: query (const std::string& name,
                                  ISvcLocator *pSvcLocator)
    : EL::AnaAlgorithm (name, pSvcLocator)
  {% for l in instance_initialization %}
  ,{{l}}
  {%- endfor %}
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  This is also where you
  // declare all properties for your algorithm.  Note that things like
  // resetting statistics variables or booking histograms should
  // rather go into the initialize() function.

  // Turn off file access statistics reporting. This is, according to Attila, useful
  // for GRID jobs, but not so much for other jobs. For those of us not located at CERN
  // and for a large amount of data, this can sometimes take a minute.
  // So we get rid of it.
  xAOD::TFileAccessTracer::enableDataSubmission(false);

  {% for l in ctor_lines %}
  {{l}}
  {% endfor %}

}

StatusCode query :: initialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.

  {% for l in book_code %}
  {{l}}
  {% endfor %}

  {% for l in initialize_lines %}
  {{l}}
  {% endfor %}

  return StatusCode::SUCCESS;
}

StatusCode query :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  {% for l in query_code %}
  {{l}}
  {% endfor %}

  return StatusCode::SUCCESS;
}



StatusCode query :: finalize ()
{
  // This method is the mirror image of initialize(), meaning it gets
  // called after the last event has been processed on the worker node
  // and allows you to finish up any objects you created in
  // initialize() before they are written to disk.  This is actually
  // fairly rare, since this happens separately for each worker node.
  // Most of the time you want to do your post-processing on the
  // submission node after all your histogram outputs have been
  // merged.
  return StatusCode::SUCCESS;
}
