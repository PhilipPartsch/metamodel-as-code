#########################
Definition of a Metamodel
#########################

Here we define a sphinx-needs metamodel.

.. needflow::
   :filter: type != "sn_option" and type != "sn_link"

Requirements
************

.. sn_typegroup:: Requirements
   :id: GROUP__requirements

   .. needflow::
      :root_id: GROUP__requirements
      :root_depth: 1

   .. needarch::

      {{flow(need().id)}}{
      {{import("groups_back")}}
      }


.. sn_type:: sys requirement
   :id: TYPE__sys_requirement
   :directive: sysreq
   :prefix: SYSREQ__
   :color: #FFA500
   :style: node
   :mandatory: OPTION__safety
   :groups: GROUP__requirements


.. sn_type:: sw requirement
   :id: TYPE__sw_requirement
   :directive: swreq
   :prefix: SWREQ__
   :color: #FFA500
   :style: node
   :mandatory: OPTION__safety
   :groups: GROUP__requirements


.. sn_type:: assumed requirement
   :id: TYPE__assumed_req
   :directive: asreq
   :prefix: ASREQ__
   :color: #FFA500
   :style: node
   :mandatory: OPTION__safety
   :groups: GROUP__requirements


Software Architecture
*********************

.. sn_typegroup:: Software Architecture
   :id: GROUP__sw_arch

   .. list2need::
      :types: sn_association

      *  (TYPE__sw_arch__satisfies__assumed_req) satisfies.
         The :need:`GROUP__sw_arch` satisfies :need:`TYPE__assumed_req`.
         ((targets="TYPE__assumed_req", link="LINK__satisfies"))
      *  (TYPE__sw_arch__covered_by__unit) covered by.
         The :need:`GROUP__sw_arch` is covered by :need:`TYPE__unit`.
         ((targets="TYPE__unit", link="LINK__covered_by"))


.. sn_type:: Software Architecture Diagram
   :id: TYPE__sw_arch_diagram
   :directive: sw_arch_dia
   :prefix: ARCH_DIA__
   :color: #FFA500
   :style: node
   :mandatory: OPTION__safety
   :groups: GROUP__sw_arch


.. sn_type:: Software Architecture Decision
   :id: TYPE__sw_arch_decision
   :directive: sw_arch_dec
   :prefix: ARCH_DEC__
   :color: #FFA500
   :style: node
   :mandatory: OPTION__safety
   :groups: GROUP__sw_arch

Safety
******

.. sn_type:: Assumption of Use
   :id: TYPE__aou
   :directive: aou
   :prefix: AOU__
   :color: #FF0000
   :style: node
   :mandatory: OPTION__safety

   .. list2need::
      :types: sn_association

      *  (TYPE__aou__satisfies__assumed_req) satisfies.
         The :need:`TYPE__aou` satisfies :need:`TYPE__assumed_req`.
         ((targets="TYPE__assumed_req", link="LINK__satisfies"))
      *  (TYPE__aou__satisfies__sw_arch) satisfies.
         The :need:`TYPE__aou` satisfies :need:`GROUP__sw_arch`.
         ((targets="GROUP__sw_arch", link="LINK__satisfies"))


.. sn_option:: safety
   :id: OPTION__safety
   :name: safety
   :description: safety level
   :schema: {"type": "string", "enum": ["QM", "ASIL-A", "ASIL-B", "ASIL-C", "ASIL-D"]}

   The safety option indicates the safety level of a need.


Testing
*******


.. sn_type:: test_specification
   :id: TYPE__test_specification
   :directive: test_specification
   :prefix: TESTSPEC__
   :color: #00FF00
   :style: node
   :mandatory: OPTION__safety

   A test specification describes a need that defines tests for requirements.

   .. list2need::
      :types: sn_association

      *  (TYPE__test_specification__verifies) verifies.
         The test_specification verifies requirements.
         ((targets="GROUP__requirements", link="LINK__verifies"))


Software Architecture II
************************

.. sn_typegroup:: Software Architecture II
   :id: GROUP__sw_arch2


.. sn_type:: Unit
   :id: TYPE__unit
   :directive: unit
   :prefix: UNIT__
   :color: #FFA500
   :style: node
   :mandatory: OPTION__safety
   :groups: GROUP__sw_arch2

   .. list2need::
      :types: sn_association

      *  (TYPE__unit__provided) provided.
         The unit provided port.
         ((targets="TYPE__port", link="LINK__provided"))

      *  (TYPE__unit__required) required.
         The unit required port.
         ((targets="TYPE__port", link="LINK__required"))


.. sn_type:: Port
   :id: TYPE__port
   :directive: port
   :prefix: PORT__
   :color: #FFA500
   :style: node
   :mandatory: OPTION__safety
   :groups: GROUP__sw_arch2

.. sn_type:: Parameter
   :id: TYPE__parameter
   :directive: parameter
   :prefix: PORT__
   :color: #FFA500
   :style: node
   :groups: GROUP__sw_arch2

.. sn_type:: Datatype
   :id: TYPE__datatype
   :directive: datatype
   :prefix: DATATYPE__
   :color: #FFA500
   :style: node
   :groups: GROUP__sw_arch2


Options
*******




Links
*****

.. sn_link:: verifies
   :id: LINK__verifies
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

.. sn_link:: satisfies
   :id: LINK__satisfies
   :option: satisfies
   :incoming: satisfied by
   :outgoing: satisfies
   :copy: true
   :allow_dead_links: false
   :style: #000000
   :style_part: #000000
   :style_start: -
   :style_end: ->

   A "satisfies" link indicates that a element satisfies another element.


.. sn_link:: covers
   :id: LINK__covers
   :option: covers
   :incoming: covered by
   :outgoing: covers
   :copy: true
   :allow_dead_links: false
   :style: #000000
   :style_part: #000000
   :style_start: -
   :style_end: ->

   A "covers" link indicates that a element covers another element.

.. sn_link:: covered_by
   :id: LINK__covered_by
   :option: covered_by
   :incoming: covers
   :outgoing: covered by
   :copy: true
   :allow_dead_links: false
   :style: #000000
   :style_part: #000000
   :style_start: -
   :style_end: ->

   A "covered_by" link indicates that a element is covered by another element.

.. sn_link:: provided
   :id: LINK__provided
   :option: provided
   :incoming: provided by
   :outgoing: provided
   :copy: true
   :allow_dead_links: false
   :style: #000000
   :style_part: #000000
   :style_start: -
   :style_end: ->

   A "provided" link indicates that a element is provided another element.

.. sn_link:: required
   :id: LINK__required
   :option: required
   :incoming: required by
   :outgoing: required
   :copy: true
   :allow_dead_links: false
   :style: #000000
   :style_part: #000000
   :style_start: -
   :style_end: ->

   A "required" link indicates that a element is required another element.

.. sn_link:: datatype
   :id: LINK__datatype
   :option: datatype
   :incoming: datatype of
   :outgoing: datatype
   :copy: true
   :allow_dead_links: false
   :style: #000000
   :style_part: #000000
   :style_start: -
   :style_end: ->

   A "optinal" link indicates that a element is optinal of another element.


