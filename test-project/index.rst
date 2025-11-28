#########################
Test Project
#########################

Here we define a sphinx-needs test-project for our metamodel.


.. asreq:: Assumed Requirement 1
   :id: ASREQ__1
   :safety: ASIL-B

.. sw_arch_dia:: Software Architecture Diagram 1
   :id: SW_ARCH_DIA__1
   :safety: ASIL-B
   :satisfies: ASREQ__1

.. aou:: Assumption of Use 1
   :id: AOU__1
   :safety: ASIL-B
   :satisfies: ASREQ__1, SW_ARCH_DIA__1

