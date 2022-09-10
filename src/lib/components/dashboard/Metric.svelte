<script lang="ts">
	import { Column, Row, Tile } from 'carbon-components-svelte';

	export let title: string;
	export let metric: string | number;
	export let prefix: string = '';
</script>

<Tile>
	<Row><Column><p>{title}</p></Column></Row>
	<Row><Column><h2>{prefix}{metric}</h2></Column></Row>
</Tile>

<style>
	h2 {
		text-align: center;
	}
</style>
