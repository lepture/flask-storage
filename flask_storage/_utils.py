class ConfigItem(object):
    """The configuration item which may be bound with a instance.

    :param name: the property name.
    :param namespace: optional. the name of the attribute which contains all
                      configuration nested in the instance.
    :param default: optional. the value which be provided while the
                    configuration item has been missed.
    :param required: optional. if this paramater be ``True`` , getting missed
                     configuration item without default value will trigger a
                     ``RuntimeError`` .
    """

    def __init__(self, name, namespace="config", default=None, required=False):
        self.name = name
        self.namespace = namespace
        self.default = default
        self.required = required

    def __repr__(self):
        template = "ConfigItem(%r, namespace=%r, default=%r, required=%r)"
        return template % (self.name, self.name, self.default, self.required)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        namespace = self._namespace(instance)
        if self.name not in namespace and self.required:
            raise RuntimeError("missing %s['%s'] in %r" %
                               (self.namespace, self.name, instance))
        return namespace.get(self.name, self.default)

    def __set__(self, instance, value):
        namespace = self._namespace(instance)
        namespace[self.name] = value

    def _namespace(self, instance):
        """Gets exists namespace or creates it."""
        if not hasattr(instance, self.namespace):
            setattr(instance, self.namespace, {})
        return getattr(instance, self.namespace)
