<script lang="ts">
	import { OutboundLink } from 'carbon-components-svelte';
</script>

<h1>Welcome</h1>

<h4>This is a demo application built for the <b>Getting Stuff Done With Data</b> conference.</h4>

<h5>In the Grid Menu (top right) you'll find links to different applications.</h5>

<p>
	This demo was built by <OutboundLink href="tinybird.co">Tinybird</OutboundLink>. You can sign up
	for free and start building your own applications over realtime data.
</p>

<div>
	<img src="tinybirdlogo.png" />
</div>

<style>
	h1,
	h4,
	h5,
	p {
		text-align: center;
	}
	h4,
	h5,
	p {
		padding-top: 1rem;
	}
	h4 > b {
		font-weight: bold;
	}
	img {
		padding-top: 2rem;
		max-width: 200px;
		display: block;
		margin-left: auto;
		margin-right: auto;
		width: 50%;
	}
</style>
