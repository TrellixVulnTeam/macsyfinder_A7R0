# -*- coding: utf-8 -*-

################################################################################
# MacSyFinder - Detection of macromolecular systems in protein datasets        #
#               using systems modelling and similarity search.                 #
# Authors: Sophie Abby, Bertrand Neron                                         #
# Copyright (c) 2014-2019  Institut Pasteur (Paris) and CNRS.                  #
# See the COPYRIGHT file for details                                           #
#                                                                              #
# MacsyFinder is distributed under the terms of the GNU General Public License #
# (GPLv3). See the COPYING file for details.                                   #
################################################################################

from typing import List


def get_models_name_to_detect(models, model_registry) -> List[str]:
    """
    :param models: the list of models to detect as returned by config.models.
    :type models: list of tuple with the following structure:
                  [('model_1', ('def1, def2, ...)), ('model_2', ('def1', ...)), ...]
    :param model_registry: the models registry for this run.
    :type model_registry: :class:`macsypy.registries.ModelRegistry` object.
    :return: the models fully qualified name to launch a detection on.
    :rtype: list of string ['model_1/def1', 'model_1/def2', ..., 'model_2/def1', ...]
    :raise ValueError: if a model name provided in models is not in model_registry.
    """
    models_name_to_detect = []
    for group_of_defs in models:
        root = group_of_defs[0]
        definitions = group_of_defs[1]
        model_loc = model_registry[root.split('/')[0]]
        if 'all' in [d.lower() for d in definitions]:
            if root == model_loc.name:
                root = None
            def_loc = model_loc.get_all_definitions(root_def_name=root)
            models_name_to_detect.extend([d.fqn for d in def_loc])
        else:
            models_name_to_detect.extend([model_loc.get_definition('{}/{}'.format(root, one_def)).fqn
                                          for one_def in definitions])
    return models_name_to_detect
