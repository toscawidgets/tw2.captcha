<%namespace name="tw" module="tw2.core.mako_util"/>
<span id="${w.attrs['id']}:wrapper">
	<img id="${w.attrs['id']}_img"
		src="${w.controller_prefix}/image/${w.payload}"/>
	<input type="text" ${tw.attrs(attrs=w.attrs)}/>
</span>
