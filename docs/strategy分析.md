# Python 类

##### 基类和子类得关系

在面向对象编程中，基类和子类是两个重要的概念，用于描述类之间的继承关系。

基类（也称为父类或超类）是一个通用的类，它定义了一组共享的属性和方法。基类可以被一个或多个子类继承，子类可以使用基类的属性和方法，并且可以通过重写或添加新的属性和方法来扩展基类的功能。

子类是通过继承基类而创建的新类。子类继承了基类的属性和方法，并且可以根据需要进行修改、扩展或重新定义。子类可以具有自己独特的属性和方法，同时也可以使用基类的属性和方法。

举例说明：

假设我们有一个基类叫做Animal（动物），它有一个属性叫做name（名字）和一个方法叫做speak（说话）。基类Animal定义了所有动物都具有的共同特征。

现在我们创建一个子类叫做Dog（狗），它继承了Animal基类。Dog子类可以使用Animal基类中定义的属性name和方法speak，并且可以根据需要添加自己的独特属性和方法，比如bark（吠叫）。

代码示例：

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("I am an animal.")

class Dog(Animal):
    def bark(self):
        print("Woof!")

animal = Animal("Animal")
animal.speak()  # 输出: I am an animal.

dog = Dog("Buddy")
dog.speak()  # 输出: I am an animal.
dog.bark()  # 输出: Woof!
```

在上述示例中，Animal是基类，Dog是子类。Dog继承了Animal的属性name和方法speak，并且添加了自己的方法bark。通过创建Dog的实例，我们可以调用基类和子类中定义的方法。

总结：基类和子类之间的关系可以被看作是一种继承关系，子类继承了基类的属性和方法，并且可以根据需要进行修改和扩展。这种继承关系使得代码可以更加模块化、可重用，并且能够更好地组织和管理对象之间的关系。

##### 如何去规划基类

规划基类并考虑子类的可用性需要遵循一些设计原则和方法。以下是一些常用的设计方法：

1. 单一职责原则（SRP）：基类应该只负责一个单一的职责或功能，这样可以确保基类的设计简洁和高内聚。如果一个基类具有多个不相关的职责，可能会导致子类在使用时出现混乱或冗余。

2. 开放封闭原则（OCP）：基类应该是开放扩展的，但封闭修改的。这意味着可以通过扩展子类来增加新的功能，而无需修改基类的代码。这样可以确保基类的稳定性和可维护性。

3. Liskov替换原则（LSP）：子类应该能够完全替代其基类，并且可以在不产生错误或异常的情况下使用。这意味着子类不应该改变基类已经定义的行为，而只能进行扩展或重写。

4. 依赖倒置原则（DIP）：基类应该依赖于抽象而不是具体的实现。这样可以使得子类更加灵活，可以根据需要选择不同的具体实现。

5. 接口隔离原则（ISP）：基类应该定义适合子类使用的最小接口。这样可以避免子类不必要地实现或依赖于不需要的方法。

在规划基类时，需要考虑以下因素来确保子类的可用性：

- 提供清晰、简洁和易于理解的接口，使得子类能够轻松地使用基类的功能。
- 尽量将共享的属性和方法放在基类中，以避免子类重复实现相同的代码。
- 考虑子类可能的特殊需求，并根据需要提供扩展或重写基类的方法。
- 遵循面向对象设计原则和最佳实践，以确保基类和子类之间的关系清晰、稳定和可维护。

通过合理规划基类并考虑子类的可用性，可以提高代码的可扩展性、可维护性和可重用性，同时减少潜在的错误和冗余代码。

##### 如何重写

重写是指在子类中重新定义或修改基类中已经存在的方法。通过重写，子类可以根据自身的需求来定制或扩展基类的行为。

在以下情况下，可以考虑对基类的方法进行重写：

1. 修改行为：子类需要对基类的方法进行修改以适应特定的需求。例如，基类的方法可能提供了一个通用的实现，但子类需要根据自己的逻辑来修改部分行为。

2. 扩展功能：子类需要在基类的方法上添加额外的功能。通过重写基类的方法，子类可以在调用基类方法之前或之后执行一些额外的操作。

3. 适应特殊需求：子类可能有一些特殊的需求，需要对基类方法进行定制以满足这些需求。重写可以允许子类根据自己的特殊情况来重新定义方法的实现。

4. 实现抽象方法：如果基类中定义了一个抽象方法（即只有方法签名而没有具体实现），则子类必须重写该方法以提供具体的实现。

在进行重写时，需要注意以下几点：

- 方法签名必须与基类中被重写的方法相同，包括参数列表和返回类型。
- 子类中重写的方法应该使用`super()`来调用基类中被重写的方法，以确保基类的行为仍然得到执行。
- 重写的方法可以完全覆盖基类的实现，也可以在基类的实现上进行扩展。

重写基类的方法可以使子类更加灵活和适应特定的需求，但需要谨慎使用。过多的重写可能会导致代码混乱和难以维护。因此，在进行重写时，需要仔细考虑是否真正需要修改基类方法，并确保子类的行为与基类保持一致性。

##### 子类进行初始化时，必须调用super().__init__嘛

在大多数情况下，子类在进行初始化时，确实需要调用基类的构造函数（即`super().__init__()`）。这是因为子类继承了基类的属性和方法，而基类的构造函数负责初始化这些属性。

通过调用`super().__init__()`，子类可以确保基类的构造函数被正确地执行。这样可以保证子类对象在创建时具有基类的属性，并且可以在子类的构造函数中添加额外的逻辑。

需要注意的是，如果子类没有定义自己的构造函数，则会默认继承基类的构造函数。在这种情况下，不需要显式调用`super().__init__()`，因为Python会自动执行基类的构造函数。

然而，如果子类定义了自己的构造函数，并且希望继承基类的初始化逻辑，就需要在子类的构造函数中显式调用`super().__init__()`。这样可以确保基类的初始化代码得到执行，并且可以在子类中添加自己的初始化逻辑。

总之，在大多数情况下，子类在进行初始化时应该调用`super().__init__()`来确保基类的构造函数被正确执行。但也要根据具体情况来判断是否需要调用基类的构造函数。

##### @abc.abstractmethod

`@abc.abstractmethod` 是 Python 中的一个装饰器，用于声明一个抽象方法。抽象方法是一种只有方法的签名而没有具体实现的方法，它必须在子类中进行实现才能被调用。

`abc` 是 Python 内置的模块 `abc` 的缩写，它提供了抽象基类（Abstract Base Class）的功能。抽象基类是一种特殊的类，它定义了一组抽象方法，用于规范子类的行为。子类必须实现这些抽象方法才能被实例化。

在使用 `@abc.abstractmethod` 装饰器时，需要满足以下两个条件：

1. 在声明该方法所在的类之前，需要通过 `class ClassName(ABC):` 的方式来继承 `ABC` 类。
2. 在希望声明为抽象方法的方法上方添加 `@abc.abstractmethod` 装饰器。

通过使用 `@abc.abstractmethod` 装饰器，我们可以在基类中定义一组抽象方法，然后在子类中强制实现这些方法。这样可以确保子类具有相同的接口和行为，提高代码的可读性和可维护性。如果子类没有实现基类中的所有抽象方法，则在实例化子类时会引发 `TypeError` 异常。

```yaml
data_handler_config: &data_handler_config
    start_time: 2008-01-01
    end_time: 2020-08-01
    fit_start_time: 2008-01-01
    fit_end_time: 2014-12-31
    instruments: *market
```

在上述代码中，`&data_handler_config`和`*market`是YAML语言中的特殊用法。

`&data_handler_config`是YAML中的锚点（Anchor），它用于标记一个数据结构，以便在其他位置进行引用。在这里，`&data_handler_config`标记了一个名为`data_handler_config`的数据结构。

`*market`是YAML中的引用（Alias），它用于在其他位置引用之前定义的锚点。在这里，`*market`引用了之前定义的锚点`&data_handler_config`，表示使用相同的值。

因此，在这段代码中，`&data_handler_config`标记了一个名为`data_handler_config`的数据结构，而`*market`则表示在其他位置使用与之前定义的锚点相同的值。这种方式可以避免重复定义相同的值，并提高代码的可读性和维护性。



```python
交易决策由策略进行制定，并由执行器执行。

Motivation:
动机：
    Here are several typical scenarios for `BaseTradeDecision`

    以下是`BaseTradeDecision`的几种典型情况：

    Case 1:
    情况1：
    1. 外部策略做出决策。该决策在当前时间段的开始时不可用。
    2. 经过一段时间后，决策得到更新并变得可用。
    3. 内部策略试图获取决策，并根据`get_range_limit`开始执行决策。

    Case 2:
    情况2：
    1. 外部策略的决策在时间段开始时可用。
    2. 同情况1的第3步。

"""

def __init__(self, strategy: BaseStrategy, trade_range: Union[Tuple[int, int], TradeRange, None] = None) -> None:
    """
    参数
    ----------
    strategy : BaseStrategy
        制定决策的策略
    trade_range: Union[Tuple[int, int], Callable] (optional)
        底层策略的索引范围。

        下面是每种类型的trade_range的两个示例：

        1) Tuple[int, int]
        底层策略的起始索引和结束索引（两端都包括）

        2) TradeRange

    """
    self.strategy = strategy
    self.start_time, self.end_time = strategy.trade_calendar.get_step_time()
    # 上层策略对_sub_trading的初始化之前，上层策略对_sub_trading没有关于子执行器的知识
    self.total_step: Optional[int] = None
    if isinstance(trade_range, tuple):
        # 对于Tuple[int, int]
        trade_range = IdxTradeRange(*trade_range)
    self.trade_range: Optional[TradeRange] = trade_range

def get_decision(self) -> List[DecisionType]:
    """
    获取**具体决策**（例如执行订单）
    这将由内部策略调用

    返回
    -------
    List[DecisionType:
        决策结果。通常是一些订单
        示例：
            []:
                决策不可用
            [concrete_decision]:
                可用
    """
    raise NotImplementedError(f"This type of input is not supported")

def update(self, trade_calendar: TradeCalendarManager) -> Optional[BaseTradeDecision]:
    """
    在每个步骤的**开始**时调用。

    此函数用于以下目的：
    1）为制定`self`决策的策略留下一个更新决策自身的钩子
    2）从内部执行器日历中更新一些信息

    参数
    ----------
    trade_calendar : TradeCalendarManager
        **内部策略**的日历！！！

    返回
    -------
    BaseTradeDecision:
        新的更新，使用新的决策。如果没有更新，则返回None（使用先前的决策（或不可用））
    """
    # 目的1）
    self.total_step = trade_calendar.get_trade_len()

    # 目的2）
    return self.strategy.update_trade_decision(self, trade_calendar)

def _get_range_limit(self, **kwargs: Any) -> Tuple[int, int]:
    if self.trade_range is not None:
        return self.trade_range(trade_calendar=cast(TradeCalendarManager, kwargs.get("inner_calendar")))
    else:
        raise NotImplementedError("The decision didn't provide an index range")

def get_range_limit(self, **kwargs: Any) -> Tuple[int, int]:
    """
    返回限制决策执行时间的预期步骤范围
    左右两端都**包括**

    如果没有可用的trade_range，则返回`default_value`

    仅在`NestedExecutor`中使用
    - 最外层策略将不遵循任何范围限制（但它可能会给出范围限制）
    - 最内层策略的range_limit将无效，因为原子执行器没有这样的特性。

    **注意**：
    1）在以下情况下必须在`self.update`之后调用此函数（由NestedExecutor确保）：
    - 用户依赖于`self.update`的自动剪辑功能

    2）在NestedExecutor中的_init_sub_trading之后将调用此函数。

    参数
    ----------
    **kwargs:
        {
            "default_value": <default_value>, # 使用字典是为了区分未提供值或提供了None
            "inner_calendar": <inner strategy的交易日历>
            # 因为range_limit将控制内部策略的步骤范围，所以当trade_range是可调用的时，inner_calendar将是一个
            # 重要参数
        }

    返回
    -------
    Tuple[int, int]:

    Raises
    ------
    NotImplementedError:
        如果满足以下条件
        1）决策无法提供统一的开始和结束
        2）未提供default_value
    """
    try:
        _start_idx, _end_idx = self._get_range_limit(**kwargs)
    except NotImplementedError as e:
        if "default_value" in kwargs:
            return kwargs["default_value"]
        else:
            # 默认获取完整索引
            raise NotImplementedError(f"The decision didn't provide an index range") from e

    # 剪辑索引
    if getattr(self, "total_step", None) is not None:
        # 如果调用了`self.update`。
        # 那么_start_idx，_end_idx应该被剪辑
        assert self.total_step is not None
        if _start_idx < 0 or _end_idx >= self.total_step:
            logger = get_module_logger("decision")
            logger.warning(
                f"[{_start_idx},{_end_idx}]超出total_step({self.total_step})，它将被剪辑。",
            )
            _start_idx, _end_idx = max(0, _start_idx), min(self.total_step - 1, _end_idx)
    return _start_idx, _end_idx

def get_data_cal_range_limit(self, rtype: str = "full", raise_error: bool = False) -> Tuple[int, int]:
    """
    基于数据日历获取范围限制

    注意：这是**总**范围限制，而不仅仅是一个步骤

    做出以下假设
    1）common_infra中交易的频率与数据日历相同
    2）用户希望按**天**（即240分钟）对索引进行模运算

    参数
    ----------
    rtype: str
        - "full"：返回一天内决策的完整限制
        - "step"：返回当前步骤的限制

    raise_error: bool
        True：如果没有设置trade_range，则抛出错误
        False：返回完整的交易日历。

        在以下情况下很有用
        - 用户希望在没有决策级别交易范围可用时遵循特定订单的交易时间范围。抛出NotImplementedError以指示范围限制不可用

    返回
    -------
    Tuple[int, int]:
        数据日历中的范围限制

    Raises
    ------
    NotImplementedError:
        如果满足以下条件
        1）决策无法提供统一的开始和结束
        2）raise_error为True
    """
    # 潜在的性能问题
    day_start = pd.Timestamp(self.start_time.date())
    day_end = epsilon_change(day_start + pd.Timedelta(days=1))
    freq = self

```

```python
参数
----------
time_per_step：str
    每个交易步骤的交易时间，用于生成交易日历
show_indicator：bool，可选
    是否显示指标：
    - 'pa'，价格优势（price advantage）
    - 'pos'，正收益率（positive rate）
    - 'ffr'，成交率（fulfill rate）
indicator_config：dict，可选
    用于计算交易指标的配置，包括以下字段：
    - 'show_indicator'：是否显示指标，可选，默认为False。指标包括：
        - 'pa'，价格优势
        - 'pos'，正收益率
        - 'ffr'，成交率
    - 'pa_config'：价格优势的配置，可选
        - 'base_price'：交易价格相对于基准价格的提升值，可选，默认为'twap'
            - 如果'base_price'为'twap'，基准价格为时间加权平均价格
            - 如果'base_price'为'vwap'，基准价格为成交量加权平均价格
        - 'weight_method'：计算每个步骤中不同订单价格优势的总体价格优势时的加权方法，可选，默认为'mean'
            - 如果'weight_method'为'mean'，计算不同订单价格优势的均值
            - 如果'weight_method'为'amount_weighted'，计算不同订单价格优势的按金额加权平均值
            - 如果'weight_method'为'value_weighted'，计算不同订单价格优势的按价值加权平均值
    - 'ffr_config'：成交率的配置，可选
        - 'weight_method'：计算每个步骤中不同订单成交率的总体成交率时的加权方法，可选，默认为'mean'
            - 如果'weight_method'为'mean'，计算不同订单成交率的均值
            - 如果'weight_method'为'amount_weighted'，计算不同订单成交率的按金额加权平均值
            - 如果'weight_method'为'value_weighted'，计算不同订单成交率的按价值加权平均值
示例：
{
    'show_indicator': True,
    'pa_config': {
        "agg": "twap",  # "vwap"
        "price": "$close",  # 默认使用交易所的成交价格
    },
    'ffr_config': {
        'weight_method': 'value_weighted',
    }
}

generate_portfolio_metrics：bool，可选
    是否生成投资组合指标，默认为False
verbose：bool，可选
    是否打印交易信息，默认为False
track_data：bool，可选
    是否生成交易决策数据，在训练强化学习代理时使用
    - 如果self.track_data为True，在生成训练数据时，`execute`方法的输入`trade_decision`将由`collect_data`生成
    - 否则，`trade_decision`将不会生成

trade_exchange：Exchange
    提供市场信息的交易所，用于生成投资组合指标
    - 如果generate_portfolio_metrics为None，则忽略trade_exchange
    - 否则，如果`trade_exchange`为None，则将self.trade_exchange设置为common_infra中的交易所

common_infra：CommonInfrastructure，可选
    用于回测的公共基础设施，可能包括：
    - trade_account：Account，可选，用于交易的账户
    - trade_exchange：Exchange，可选，提供市场信息的交易所

settle_type：str
    请参阅BasePosition.settle_start的文档
``

```

