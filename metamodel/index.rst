#########################
Definition of a Metamodel
#########################

Here we define a sphinx-needs metamodel.

Types
*****

.. sn_typegroup:: requirements
   :id: SN_TYPE__requirements


.. sn_type:: sw requirement
   :id: SN_TYPE__sw_requirement
   :directive: requirement
   :prefix: REQ__
   :color: #FFA500
   :style: node
   :mandatory: SN_OPTION__safety
   :optinal: SN_OPTION__priority
   :groups: SN_TYPE__requirements

   A requirement describes a need that has to be fulfilled.


.. sn_type:: test_specification
   :id: SN_TYPE__test_specification
   :directive: test_specification
   :prefix: TESTSPEC__
   :color: #00FF00
   :style: node
   :mandatory: SN_OPTION__safety, SN_LINK__verifies
   :optinal: SN_OPTION__priority

   A test specification describes a need that defines tests for requirements.

   .. list2need::
      :types: sn_association

      * (SN_TYPE__test_specification__verifies) verifies link.
        The test_specification verifies requirements.
        ((targets="SN_TYPE__requirements", link="SN_LINK__verifies"))

   .. sn_association:: verifies2
      :id: SN_TYPE__test_specification__verifies2
      :targets: SN_TYPE__requirements
      :link: SN_LINK__verifies


Options
*******

.. sn_option:: priority
   :id: SN_OPTION__priority
   :name: priority

   : description : Priority of the need

   The priority option indicates the importance of a need.


.. sn_option:: safety
   :id: SN_OPTION__safety
   :name: safety

   : description : safety level

   The safety option indicates the safety level of a need.


Links
*****

.. sn_link:: verifies
   :id: SN_LINK__verifies
   :option: verifies
   :incoming: verified by
   :outgoing: verifies
   :copy: true
   :allow_dead_links: false
   :style: #000000
   :style_part: #000000
   :style_start: -
   :style_end: ->

   A "verifies" link indicates that a test specification verifies a requirement.
