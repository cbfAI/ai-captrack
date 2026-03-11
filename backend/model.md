Qwen3.5-397B-A17B API文档
更新时间： 2026-02-18 21:33:46
Qwen3.5-397B-A17B
Qwen3.5-397B-A17B是Qwen3.5 开源系列旗舰大语言模型，支持文本和多模态任务。

接口描述
通过调用本接口，来实现对Qwen3.5-397B-A17B的对话请求


域名列表
调用不同云区域的模型，请使用不同的域名

支持的云区域	域名
上海二十二区
联系客户经理获取
贵阳基地二区	https://aigw-gzgy2.cucloud.cn:8443


鉴权说明

服务使用api key进行鉴权。

api key获取方式：控制台创建服务，然后创建api key，创建时关联api key与服务。

请求头域
除公共头域外，增加了apikey头域。

请求参数
Body参数



名称	类型	是否必填	描述
model	string	是	使用的模型名称
messages	List(message)	是	消息列表，其中每条消息必须包含 role和 content。
temperature	float	否	控制生成的文本的创造性。较高的值（如 0.8）将使输出更随机，而较低的值（如 0.2）则更加集中和确定。
top_p	float	否	一种替代 temperature 的采样方法。top_p 会根据累积概率选择 token，1 表示考虑所有 token。
n	int	否	生成的回复数量
stream	bool	否	是否开启流式响应。若为 true，响应会逐步返回部分内容。
stop	List(string)	否	停止生成的字符串，支持字符串数组（如 ["\n"]）。
max_tokens	int	否	单次请求生成的最大 token 数。
presence_penalty	int	否	是否鼓励生成新主题。值为 -2.0 至 2.0 之间，正值增加生成新话题的可能性。
frequency_penalty	int	否	控制生成重复 token 的可能性。值为 -2.0 至 2.0 之间，正值减少重复。
logit_bias	int	否	用于调整特定 token 出现的概率。接受一个 map，key 是 token 的 ID，值是从 -100 到 100 的数值。
user	string	否	用户 ID，用于标识请求来源的用户。




message说明



名称	类型	是否必填	描述
role	string	是	角色，包括以下： system：用于设定助手的行为，如“你是一个帮助用户解决问题的助手”。 user：表示用户输入 assistant：表示助手回复
content	string	是	对话内容