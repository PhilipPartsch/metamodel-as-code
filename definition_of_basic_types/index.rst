#########################
Definition of Basic Types
#########################

Here we define the baisc types of a sphinx-needs metamodel.


.. need:: Type
   :id: SN_TYPE
   :sn_links: optinal, mandatory
   :sn_attributes: directive,
                title,
                prefix,
                color,
                style

   A Sphinx-Needs metamodel has to define the types it wants to be used.

   https://sphinx-needs.readthedocs.io/en/latest/configuration.html#needs-types



.. need:: Extra Option
   :id: SN_OPTION
   :sn_attributes: name,
                description

   https://sphinx-needs.readthedocs.io/en/latest/configuration.html#needs-extra-options

   todo:
   {
   "name": "efforts",
   "description": "Efforts in days",
   "schema": {
   "type": "integer",
   "mininum": 0,
   },
   }


.. need:: Extra Link
   :id: SN_LINK
   :sn_attributes: option,
                incoming,
                outgoing,
                copy,
                allow_dead_links,
                style,
                style_part,
                style_start,
                style_end

   https://sphinx-needs.readthedocs.io/en/latest/configuration.html#needs-extra-links




