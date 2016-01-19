Steps to add plugin into ceilometer
===================================

entry points
------------

(ex: /usr/lib/python2.7/dist-packages/ceilometer-2015.1.2.egg-info/entry_points.txt)

.. code-block:: bash

    [ceilometer.poll.central]  
        ...
        cloudkitty.rating = ceilometer.rating.cloudkitty:RatingCostPollster

adjust /etc/ceilometer/pipeline.yaml
------------------------------------

.. code-block:: bash

    sources:
        - name: meter_source
        interval: 600
        meters:
            - "*"
            - "!cloudkitty.rating"
      sinks:
          - meter_sink
        ...
        - name: rating_source
        interval: 1800
        meters:
            - "cloudkitty.rating"
        sinks:
            - meter_sink




